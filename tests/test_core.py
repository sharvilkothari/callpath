from dataclasses import asdict
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree

from callpath import metrics, storage
from callpath.model import Load, Profile, configure
from callpath.report import aggregate, compatibility_warnings

ROOT = Path(__file__).resolve().parent.parent


class ProfileTests(unittest.TestCase):
    def test_baseline_preserves_traffic_placement_limit_and_seed(self):
        impaired = Profile(delay_ms=80, jitter_ms=10, loss_pct=1, queue_limit=737,
                           traffic="rtp", path="both", placement="ingress", seed=1234)
        self.assertEqual(impaired.netem(), [
            "limit", "737", "delay", "80ms", "10ms", "distribution", "normal",
            "loss", "random", "1%", "seed", "1234",
        ])
        base = impaired.baseline()
        self.assertFalse(base.impaired)
        self.assertEqual(base.netem(), ["limit", "737"])
        for field in ("traffic", "path", "placement", "queue_limit", "seed"):
            self.assertEqual(getattr(base, field), getattr(impaired, field))

    def test_burst_and_invalid_input(self):
        _, burst, repeats = configure("S5", {}, {"burst_start_pct": 2})
        self.assertEqual(repeats, 5)
        self.assertIn("gemodel", burst.netem())
        for overrides in ({"delay_ms": True}, {"jitter_ms": 1}, {"loss_pct": float("nan")},
                          {"seed": 0}, {"path": "external"}, {"burst_start_pct": 1, "loss_pct": 1}):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                Profile(**overrides)
        with self.assertRaises(ValueError):
            Load(100, 21, 3, 1500, 55)


class EvidenceTests(unittest.TestCase):
    def test_latency_is_nearest_rank_from_real_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sipp-stats.csv").write_text(
                "OutgoingCall(C);SuccessfulCall(C);FailedCall(C);CallRate(C);CurrentCall\n"
                "2;0;0;1.2;2\n2;1;1;0.4;0\n")
            (root / "sipp_rtt.csv").write_text(
                "Date_ms;response_time_ms;rtd_no\n1;50;invite\n2;70;invite\n3;2;bye\n")
            values = metrics.sipp_metrics(root, Load(2, 1, 2, 1000, 25))
        self.assertEqual(values["call_setup_latency_p50_ms"]["value"], 50)
        self.assertEqual(values["call_setup_latency_p95_ms"]["value"], 70)
        self.assertEqual(values["concurrent_calls_peak"]["value"], 2)
        self.assertEqual(values["scenario_success_rate"]["value"], 0.5)
        self.assertIsNone(values["sip_retransmits"]["value"])

    def test_capture_truncation_is_unavailable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sender.pcap").touch()
            (root / "sender.log").write_text(
                "21 packets captured\n25 packets received by filter\n0 packets dropped by kernel\n")
            have, codes, reason = metrics.packets(root, "sender")
            self.assertIsNone(have)
            self.assertIsNone(codes)
            self.assertIn("incomplete", reason)

    def test_rtp_loss_duplicates_rollover_and_jitter(self):
        Packet = metrics.Packet
        sent = [Packet(0, 65535, 2**32 - 160, b"a"), Packet(0.02, 0, 0, b"b"),
                Packet(0.04, 1, 160, b"c")]
        rx = [Packet(0.01, 65535, 2**32 - 160, b"a"), Packet(0.05, 1, 160, b"c"),
              Packet(0.051, 1, 160, b"c")]
        values = metrics.stream_metrics(sent, rx)
        self.assertEqual((values["sent"], values["missing"], values["duplicates"]), (3, 1, 1))
        self.assertAlmostEqual(values["jitter_ms"], 0)

    def test_echo_rtt_does_not_match_ambiguous_payloads(self):
        Packet = metrics.Packet
        tx = {(6000, 10000, 1): [Packet(1, 0, 0, b"a"), Packet(1.02, 1, 160, b"b"),
                                Packet(1.04, 2, 320, b"b")]}
        rx = {(10000, 6000, 2): [Packet(1.07, 0, 0, b"a"), Packet(1.08, 1, 160, b"b")]}
        coverage, rtt, count = metrics.echo_metrics(tx, rx)
        self.assertEqual((coverage, count), (0.5, 1))
        self.assertAlmostEqual(rtt, 70)

    def test_pbx_maps_dtmf_and_hangup_to_sip_dialog(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "ami.jsonl").write_text(
                '{"ready":true}\n'
                '{"event":"UserEvent","userevent":"CallPathCorrelation","runid":"demo",'
                '"sipcallid":"dialog","uniqueid":"1","linkedid":"1"}\n'
                '{"event":"DTMFEnd","direction":"Received","digit":"#","uniqueid":"1"}\n'
                '{"event":"Hangup","cause":"16","uniqueid":"1"}\n')
            records, events = metrics.pbx_metrics(path, "demo")
        self.assertEqual(records["pbx_dtmf_confirmed"]["value"], 1)
        self.assertEqual(records["hangup_causes"]["value"], {"16": 1})
        self.assertEqual({event["call_id"] for event in events}, {"dialog"})

    def test_reports_track_missing_repeats(self):
        record = {"value": 1, "unit": "ratio", "source": "sipp_csv", "direction": "uac_to_uas"}
        out = aggregate([{"condition": "baseline", "stage": "smoke", "status": "SUCCEEDED",
                          "metrics": {"scenario_success_rate": record}}], 5)
        aggregate_row = out["baseline"]["smoke"]["scenario_success_rate"]
        self.assertEqual((aggregate_row["n"], aggregate_row["expected_n"]), (1, 5))
        self.assertIsNone(aggregate_row["sample_stdev"])
        conditions = {key: {} for key in ("scenario", "target", "media", "tools", "runtime", "file_hashes")}
        a = {**conditions, "profile": asdict(Profile())}
        b = {**conditions, "profile": asdict(Profile(queue_limit=500))}
        self.assertEqual(compatibility_warnings(a, b), ["profile.queue_limit differs"])

    def test_snapshot_and_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            storage.immutable(path / "snapshot.json", {"run_id": "demo"})
            with self.assertRaises(FileExistsError):
                storage.immutable(path / "snapshot.json", {})
            item, = storage.manifest(path)
            self.assertEqual(item["sha256"], storage.sha256(path / "snapshot.json"))
            with self.assertRaises(ValueError):
                storage.run_path(path, "../outside")

    def test_scenarios_are_well_formed(self):
        for path in (ROOT / "scenarios").glob("*.xml"):
            with self.subTest(path=path):
                root = ElementTree.parse(path).getroot()
                self.assertEqual(root.tag, "scenario")
                self.assertEqual(root.find("./send").attrib["start_rtd"], "invite")


if __name__ == "__main__":
    unittest.main()

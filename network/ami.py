"""Collect a bounded subset of AMI fields over PBX namespace loopback."""
import json
import socket
import time

KEEP = {"event", "eventname", "userevent", "uniqueid", "linkedid", "runid",
        "sipcallid", "cause", "cause-txt", "digit", "direction", "extra", "channel",
        "eventtime", "result"}
EVENTS = {"UserEvent", "Hangup", "CEL", "DTMFEnd", "BlindTransfer", "Newchannel"}


def main():
    with socket.create_connection(("127.0.0.1", 5038), timeout=3) as client:
        client.settimeout(None)
        stream = client.makefile("rb")
        stream.readline()
        client.sendall(b"Action: Login\r\nUsername: callpath\r\n"
                       b"Secret: callpath-local-loopback\r\nEvents: on\r\n\r\n")
        frame = {}
        while raw := stream.readline(16384):
            line = raw.decode("utf-8", "replace").strip()
            if line:
                key, sep, value = line.partition(":")
                if sep:
                    frame[key.lower()] = value.strip()
                continue
            if frame.get("response") == "Success":
                print(json.dumps({"ready": True}), flush=True)
            if frame.get("response") == "Error":
                raise RuntimeError("AMI login rejected")
            if frame.get("event") in EVENTS:
                event = {key: value for key, value in frame.items() if key in KEEP}
                event["observed_at"] = time.time()
                print(json.dumps(event), flush=True)
            frame = {}


if __name__ == "__main__":
    main()

"""Exec SIPp with fixed lab addresses after entering the generator namespace."""
import os
import shutil
import sys

scenario, extension, run_id, calls, cps, concurrency, hold = sys.argv[1:]
os.chdir("/run/callpath-work")
shutil.copyfile(f"/opt/callpath/scenarios/{scenario}", scenario)
exe = "/usr/bin/sipp"
os.execv(exe, [
    exe, "10.200.1.3:5060", "-sf", scenario,
    "-i", "10.200.1.2", "-p", "5060", "-mi", "10.200.1.2", "-mp", "6000",
    "-s", extension, "-t", "u1", "-m", calls, "-r", cps, "-l", concurrency,
    "-d", hold, "-key", "RUN_ID", run_id, "-trace_stat", "-stf", "sipp-stats.csv",
    "-trace_rtt", "-rtt_freq", "1", "-trace_err", "-trace_counts", "-fd", "1s",
    "-nostdin", "-skip_rlimit",
])

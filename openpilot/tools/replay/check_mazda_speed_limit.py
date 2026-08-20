#!/usr/bin/env python3
import sys
from copy import deepcopy

from openpilot.selfdrive.test.process_replay import get_process_config, replay_process
from openpilot.tools.lib.logreader import LogReader, ReadMode


if len(sys.argv) != 2:
  raise SystemExit(f"Usage: {sys.argv[0]} <route>")

route = sys.argv[1]
logs = LogReader(route, default_mode=ReadMode.AUTO_INTERACTIVE)

# The standard replay republishes recorded carStateSP messages. Replay card instead so the
# current Mazda parser runs against the route CAN and produces a fresh speed limit.
card_config = deepcopy(get_process_config("card"))
card_config.subs.append("carStateSP")
output = replay_process(
  card_config,
  logs,
  custom_params={"IsMetric": True},
  disable_progress=True,
)

previous = None
for msg in output:
  if msg.which() != "carStateSP":
    continue

  speed_limit = msg.carStateSP.speedLimit
  if speed_limit != previous:
    print(f"{msg.logMonoTime / 1e9:10.3f} carStateSP.speedLimit = {speed_limit:.3f} m/s")
    previous = speed_limit

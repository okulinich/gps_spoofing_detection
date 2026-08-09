# Step 1 — From custom JSON dump to a playable ROS 2 bag

*First implementation step of the thesis. Everything here runs natively on macOS — the `rosbags` Python library writes ROS 2 bags with no ROS installation required. ROS itself is only needed from Stage 4 onward, and Stage 4 is optional for the thesis results.*

---

## Why conversion is not step one

Converting first and inspecting later is how you spend two days debugging a filter before discovering that yaw rate was in deg/s. The order is: **inventory → mapping table → converter → validate → playback → dead-reckoning sanity check.**

---

## Stage 0 — Inventory the dump

A throwaway Python script that walks the JSON and prints, per signal name:

- message count, first and last timestamp, total duration
- median rate **and the distribution of inter-message gaps** — you want to see dropouts and bursts, not just the mean
- payload keys and value ranges

The output table goes into the thesis later: *"recorded data comprises N signals over M minutes at these rates"* is a real methodology paragraph.

### Two traps to check for here

**Timestamp precision.**
If the JSON stores epoch time as a float in seconds, a double holds ~15–16 significant digits while nanosecond epoch time needs 19. Resolution below ~1 µs is silently lost the moment `json.load` parses it. Check whether timestamps are integers or strings; if they are floats, quantify the damage before deciding whether it matters. For 100 Hz IMU it is tolerable; for tight cross-sensor correlation it is not.

**Clock identity.**
Is the timestamp the sensor's *validity* time or the logger's *receive* time? These differ by 100–200 ms for GNSS, and that gap is exactly what latency compensation exists for. If both are present in the payload, keep both.

---

## Stage 1 — Write the mapping table

This is the actual deliverable of the week, and it is a **document**, not code.

| dump signal | ROS 2 type | topic | field | unit in dump | unit in ROS | notes |
|---|---|---|---|---|---|---|
| | | | | | | |

### Decisions to make explicitly and write down

**Units and conventions**
- degrees vs radians
- km/h vs m/s
- yaw rate sign convention
- heading reference: true north vs vehicle frame, clockwise vs counter-clockwise

**Frames**
- ROS follows REP-103: x forward, y left, z up; ENU for the world frame.
- ISO 8855 agrees on the body frame, which is convenient — but sensor *mounting* frames may not.
- Assign `frame_id` values now: `base_link`, `imu_link`, `gnss_link`. See also REP-105 for the frame hierarchy.

**Covariances**
- Fill `NavSatFix.position_covariance` and `Imu.*_covariance`. Do not leave zeros.
- `robot_localization` ignores or misbehaves on unset covariances, and your own EKF needs real `R` values regardless.
- If the dump carries per-fix accuracy estimates, map them. Otherwise use constants and record that choice.

**Header stamp policy**
- `header.stamp` = sensor time.
- Bag receive time = logger time if available, otherwise the same value.
- Getting this wrong means `ros2 bag play` paces off one clock while the filter reasons about another.

---

## Stage 2 — The converter

`gnss_guard_tools/dump_to_mcap.py`

Structure it as three layers:

```
JSON reader  →  canonical intermediate structs  →  ROS 2 / mcap writer
```

The intermediate layer matters: the `comma2k19` converter written later plugs into the same midpoint, and the batch runner reads the same schema. **Do not let the JSON shape leak into the rest of the system.**

```python
from rosbags.rosbag2 import Writer
# mcap storage, not sqlite3 — better random access, Foxglove reads it natively
writer = Writer(path, version=9)
```

### Target topics

| topic | type |
|---|---|
| `/gnss/fix` | `sensor_msgs/NavSatFix` |
| `/imu/data_raw` | `sensor_msgs/Imu` |
| `/odom/twist` | `geometry_msgs/TwistWithCovarianceStamped` |

### Converter hygiene

- deterministic and idempotent
- emits a small JSON sidecar with conversion stats and the **source file hash** — future-you will want to know which dump produced which bag

---

## Stage 3 — Validate the conversion (not the playback)

```bash
ros2 bag info out.mcap        # do counts and duration match Stage 0?
```

Then:

- plot the converted data with matplotlib and eyeball it against the raw JSON for a handful of messages
- open the mcap in Foxglove — it reads the file directly with no ROS running, and will show the GNSS track on a map. Fastest possible check that lat/lon did not get swapped.

---

## Stage 4 — Playback

```bash
ros2 bag play out.mcap --clock --start-paused
ros2 topic hz /imu/data_raw
ros2 topic echo /gnss/fix --once
```

- `--start-paused` avoids the discovery race that silently eats the first messages.
- Confirm the observed rates match the Stage 0 table.
- `--clock` publishes `/clock`; every node must then run with `use_sim_time`.

---

## Stage 5 — First real check: naive dead reckoning

Integrate IMU and wheel odometry forward from the first GNSS fix, and plot the result against the GNSS track.

It **will** drift. That is expected and fine. What you are looking for is whether it drifts *plausibly* — a gradual divergence — or goes sideways into a wall, which means a unit or sign error back in Stage 1.

Do this **before writing a single line of EKF.** It validates the entire chain — parsing, units, frames, timestamps — with a result visible in one plot. And it is the first figure in the thesis.

---

## Checklist

- [ ] Stage 0 inventory script written; signal table produced
- [ ] Timestamp type and precision confirmed
- [ ] Sensor time vs receive time question answered
- [ ] Mapping table written, units and signs documented
- [ ] `frame_id` values assigned
- [ ] Covariance sources decided
- [ ] Converter written with canonical intermediate layer
- [ ] Sidecar with stats and source hash emitted
- [ ] `ros2 bag info` counts match the inventory
- [ ] GNSS track visually confirmed in Foxglove
- [ ] Playback rates match
- [ ] Dead-reckoning plot produced and plausible

---

## Notes

- Keep the converter's target schema identical for work dumps and `comma2k19`, so no chapter depends on data whose IP status is unresolved.
- The ROS graph is for demo, visualisation and real-time behaviour checks. Thesis numbers come from the deterministic batch runner reading mcap directly — no middleware in the loop.
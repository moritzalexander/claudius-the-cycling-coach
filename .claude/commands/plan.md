# Training Plan — Suggest Next Workouts

Prescribe specific workouts for the coming days (default: next 3-5 days) based on current fitness, fatigue, recent training patterns, and the athlete's goals/events.

## Instructions

### Step 1: Gather Context (in parallel)

1. **Fitness summary** via `get-fitness-summary` — CTL/ATL/TSB, ramp rate
2. **Recent activities** via `get-recent-activities` (limit: 20, days_back: 14) — what training has been done
3. **Wellness data** via `get-wellness-data` — recovery signals
4. **Upcoming events** via `get-upcoming-workouts` — what's already planned on the calendar
5. **Athlete profile** via `get-athlete-profile` — current thresholds
6. **Workout library** via `get-workout-library` — available pre-built workouts

Also read the athlete memory file for current goals, target events, and preferences.

### Step 2: Pre-Prescription Gates

Before prescribing any hard workout, check these gates (inspired by coaching safety logic):

**Gate 1 — TSB Check:**
- If TSB < -25: prescribe only recovery or easy endurance. No intensity.
- If TSB < -15: limit to one moderate session, rest should be easy.
- If TSB between -15 and +5: normal training.
- If TSB > +15 for more than 5 days: athlete may be losing fitness — consider adding stimulus.

**Gate 2 — Ramp Rate:**
- If ramp rate > 7 TSS/day/week: do NOT add more load. Prescribe a lighter week.
- If ramp rate > 5: be cautious — avoid increasing further.
- If ramp rate < 3: safe to progress load.

**Gate 3 — Recent Pattern:**
- Count consecutive hard days (IF > 0.85) in the last 7 days.
- After 2 consecutive hard days: prescribe easy/recovery.
- After 3+ consecutive hard days: prescribe 1-2 rest/easy days before next intensity.
- Never prescribe more than 2 hard days in a row.

**Gate 4 — Recovery Signals:**
- If HRV is suppressed (>15% below 7-day avg) or resting HR elevated (>5 bpm): recovery day.
- If sleep < 6h for 2+ consecutive days: reduce intensity.

**Gate 5 — Deload Check:**
- If it has been 3+ weeks of progressive loading (CTL rising steadily): suggest a deload week.
- Deload = reduce volume 40-60%, maintain 1-2 short intensity sessions, focus on recovery.

### Step 3: Determine Training Phase

Based on recent training patterns and athlete goals, identify the current phase:

- **Base/Aerobic Development:** Majority of riding is Z2, building volume. Prescribe: long endurance rides, tempo progression, aerobic efficiency work.
- **Build/Sweet Spot:** Athlete is doing structured work at 84-97% FTP. Prescribe: sweet spot intervals with progressive overload (longer intervals, more sets, less rest).
- **VO2max/High Intensity:** Focus on work above threshold. Prescribe: 3-5 min intervals at 106-120% FTP, short-short intervals (30/30, 40/20).
- **Race-Specific/Peak:** Fine-tuning for an event. Prescribe: race-simulation efforts, openers, maintain but don't build.
- **Recovery/Deload:** Back off. Prescribe: easy spins, recovery rides, flexibility/mobility.

If the athlete has no explicit phase, infer from the data:
- Lots of Z2 + low TSS → Base phase
- Sweet spot and threshold work appearing → Build phase
- High-intensity intervals appearing → VO2max phase
- Tapering load before a goal date → Peak phase

### Step 4: Prescribe Workouts

For each day in the planning window:

**For endurance/Z2 rides:**
- Duration: based on available time and current fitness
- Power target: 55-75% FTP ([compute range from current FTP])
- HR cap: Z2 ceiling ([from athlete HR zones])
- Cadence guidance if relevant (85-95 rpm for efficiency)

**For structured interval sessions, use progressive overload:**

Sweet Spot progression:
- SS-1: 3×10min @ 88-93% FTP, 5min recovery
- SS-2: 3×12min @ 88-93% FTP, 4min recovery
- SS-3: 2×20min @ 88-93% FTP, 5min recovery
- SS-4: 2×25min @ 88-93% FTP, 5min recovery
- SS-5: 1×45min @ 88-93% FTP

Threshold progression:
- TH-1: 3×8min @ 95-105% FTP, 4min recovery
- TH-2: 3×10min @ 95-105% FTP, 4min recovery
- TH-3: 2×15min @ 95-105% FTP, 5min recovery
- TH-4: 2×20min @ 95-105% FTP, 5min recovery
- TH-5: 1×30-40min @ 95-100% FTP

VO2max progression:
- VO2-1: 5×3min @ 106-120% FTP, 3min recovery
- VO2-2: 5×4min @ 106-115% FTP, 3min recovery
- VO2-3: 6×3min @ 106-120% FTP, 2.5min recovery
- VO2-4: 4×5min @ 106-115% FTP, 3min recovery
- VO2-5: 3×6-8min @ 106-112% FTP, 4min recovery

Short-short VO2max (Billat-style):
- 10-15× 30s on / 30s off @ 120-130% FTP
- 8-12× 40s on / 20s off @ 115-125% FTP
- 20-30× 15s on / 15s off @ 130-150% FTP

**Determine progression level** by looking at recent interval sessions:
- What level was the last sweet spot / threshold / VO2max session?
- Did the athlete complete it successfully (good compliance, stable power)?
- If yes, advance one level. If struggled, repeat the same level.

**For each prescribed workout, include:**
- Warm-up: 15-20min progressive to Z2, then 2-3× 1min spin-ups
- Main set: specific intervals with power/HR targets in watts and bpm
- Cool-down: 10-15min easy spin, Z1
- Total estimated duration and TSS
- Purpose: one sentence explaining why this workout matters right now

### Step 5: Science Check

If prescribing a training approach that might benefit from validation:
- Use WebSearch to check latest evidence for the specific prescription type
- Integrate the finding into the recommendation
- Example: if prescribing polarized week → search "polarized training distribution cycling 2025 evidence"

### Step 6: Consider Strength Training

The athlete does lower body strength 2x/week (Mon heavy, Thu explosive) and upper body on other days. When scheduling:
- Never prescribe hard cycling intervals on lower-body strength days (legs are pre-fatigued)
- Easy Z2 rides are fine on strength days (before or after, with adequate fueling)
- Schedule the hardest cycling days on non-strength days
- Upper body days have no impact on cycling performance — these are free days for hard rides

**Before prescribing any strength session, read `memory/gym_log.json`:**
- `current` section = exact weights and progression targets for each exercise
- `sessions` section = recent history showing what was done
- Check `status` fields: `"HOLD"` or `"REINTRODUCTION"` means the exercise is injured/restricted
- Respect `next_target_*` fields — these are the prescribed weights for the next session, not arbitrary progressions
- Flag any exercise marked `"pending"` that has been skipped 2+ sessions in a row

**Current injury awareness (check gym_log for latest):**
- Deadlifts: recurring lower back flare (Apr 2 + Apr 20). Now in REINTRODUCTION phase. Do not prescribe working sets until 2+ consecutive pain-free warmup sessions confirmed.
- Back extensions (45°): continue as rehab movement.

**Pre-race openers (race-day eve rule):**
- **No sprints (5–15s maximal efforts) the day before any race.** Athlete's sprint power is a known weakness — sprint-primers deplete it rather than prime it.
- Preferred opener: 35–40 min total. Easy Z2 build (15 min, max 180W) + 3 × 30s @ 110–120% FTP (360–390W) with 2 min easy recovery + 10 min flush. Primes aerobic/VO2 system without touching neuromuscular ceiling.

### Step 7: Produce the Plan

```
## Training Plan — [date range]

**Current Status:** CTL [X] | ATL [X] | TSB [X] ([interpretation])
**Phase:** [Base / Build / VO2max / Peak / Recovery]
**Weekly TSS Target:** [range] (based on current CTL and progression goals)

### [Day 1 — Date, Day of Week]
**[Workout Name]** — [Purpose in one sentence]
- Type: [Endurance / Sweet Spot / Threshold / VO2max / Recovery]
- Duration: Xh XXmin | Est. TSS: XX
- Warm-up: 15min progressive to Z2
- Main set: [specific intervals with power/HR targets]
- Cool-down: 10min Z1
- Notes: [any context — e.g., "keep HR below 152 even if power feels easy"]

### [Day 2 — Date, Day of Week]
...

### Weekly Summary
| Day | Workout | Est. TSS | Intensity |
|-----|---------|----------|-----------|
| Mon | ... | XX | Easy/Moderate/Hard |
| ... | | | |
| **Total** | | **XXX** | |

**Projected CTL after this week:** ~[estimate]
```

### Important Rules
- Always include at least 1-2 pure rest or recovery days per week
- Never schedule >3 intensity sessions per week for a non-professional cyclist
- If in doubt, prescribe less — it is always safer to undertrain slightly than to overtrain
- Every workout must have specific power/HR targets in absolute numbers (watts, bpm), not just zone names

$ARGUMENTS: Optional: planning horizon ("next 3 days", "this week", "next week"), specific goal ("prepare for a century ride", "build VO2max"), or constraint ("only have 1 hour on Tuesday and Thursday").

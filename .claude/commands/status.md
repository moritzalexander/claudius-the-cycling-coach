# Quick Fitness & Recovery Status

Fast daily check: current fitness numbers, recovery status, and what type of training is appropriate today. Designed to be quick — pull data and give a concise verdict.

## Instructions

### Step 1: Gather Data (in parallel)

1. **Fitness summary** via `get-fitness-summary`
2. **Today's wellness** via `get-wellness-for-date` (today's date) — if no data for today, get the most recent
3. **Last 3-5 activities** via `get-recent-activities` (limit: 5, days_back: 7)

### Step 2: Assess Readiness

Evaluate readiness using this layered framework (each layer adds confidence):

**Layer 1 — Training Load (always available):**
- TSB > +15: Very fresh, may be losing fitness if prolonged
- TSB +5 to +15: Fresh, good for hard sessions or racing
- TSB -5 to +5: Neutral, can train normally
- TSB -10 to -5: Mild fatigue, moderate training ok
- TSB -20 to -10: Significant fatigue, prioritize recovery or easy sessions
- TSB < -20: Deep fatigue, recovery strongly recommended

**Layer 2 — HRV (if available):**
- Compare today's RMSSD to the 7-day rolling average
- Above average: green light for hard training
- Within normal range (±1 SD or ±10%): proceed as planned
- Below average by >10%: consider reducing intensity
- Significantly suppressed (>20% below): recovery day recommended

**Layer 3 — Resting HR (if available):**
- Within ±3 bpm of baseline: normal
- Elevated 3-5 bpm: possible fatigue or stress, proceed with caution
- Elevated >5 bpm: recovery recommended unless obvious cause (caffeine, poor sleep, illness)

**Layer 4 — Sleep (if available):**
- Duration and quality: was it sufficient?
- Poor sleep compounds other fatigue signals

**Layer 5 — Subjective (if available):**
- Fatigue, soreness, stress, mood, motivation ratings
- These are often the most sensitive indicators of readiness

**Combined Verdict:**
- If majority of available signals are positive → "Ready for hard training"
- If mixed signals → "Moderate training recommended" with explanation of which signals are concerning
- If majority negative → "Recovery day recommended" with explanation
- If only TSB is available, note that the assessment is limited

### Step 3: Produce the Report

Keep it SHORT — this is a daily glance, not an analysis essay.

```
## Status — [today's date]

**Readiness: [Ready for hard training / Moderate training / Recovery recommended]**

| Metric | Value | Signal |
|--------|-------|--------|
| CTL (fitness) | XX | [context] |
| ATL (fatigue) | XX | |
| TSB (form) | XX | [fresh/neutral/fatigued] |
| Ramp rate | X.X/week | [safe/elevated] |
| HRV (RMSSD) | XX ms | [above/normal/below avg] |
| Resting HR | XX bpm | [normal/elevated] |
| Sleep | Xh XXm | [sufficient/short] |

**Last 3 days:**
- [date]: [activity name] — [TSS] TSS, IF [value]
- [date]: [activity name] — [TSS] TSS, IF [value]
- [date]: [activity name or rest day]

**Today's suggestion:** [One specific sentence: "Good day for a Z2 endurance ride, 60-90 min at 180-240W" or "Take a rest day — TSB is -22 and HRV is suppressed" or "You're fresh — good day for threshold intervals if the schedule allows"]
```

$ARGUMENTS: None required. Optionally specify a date other than today.

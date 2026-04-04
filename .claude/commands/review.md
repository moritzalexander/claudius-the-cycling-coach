# Workout Review

Analyze a specific workout. The user provides an activity ID, a date, or a description (e.g., "yesterday's ride", "the Tuesday intervals", "my last Zwift ride").

## Step 1: Identify the Activity

- If the user provides an activity ID, use it directly.
- If they provide a date or description, use `get-recent-activities` or `search-activities` to find the matching activity. If ambiguous, show the options and ask.
- Note the activity name — it often contains clues (e.g., "3x10x40/20" = workout structure, "Zwift" = indoor).

## Step 2: Fetch Streams, Count W'bal Depletions, Generate Chart

Fetch the activity streams via `get-activity-streams` — request: watts, heartrate, cadence, velocity_smooth, altitude, time.

Then run a **single bash command** that does three things:
1. Writes the chart JSON
2. Counts W'bal depletion cycles
3. Reports the count

Use this exact script (adapt the streams file path):

```bash
cat "<STREAMS_FILE>" | python3 -c "
import json, sys
from statistics import mean

raw = json.load(sys.stdin)
data = json.loads(raw['result'])
streams = data['data']['streams']

# Write chart JSON
chart = {
    'power': streams['watts'], 'hr': streams['heartrate'],
    'cadence': streams['cadence'], 'altitude': streams['altitude'],
    'time': streams['time'],
    'ftp': 325, 'wprime': 25000,
    'hr_zones': [137, 152, 159, 170, 175, 180, 189], 'laps': []
}
with open('/tmp/workout_streams.json', 'w') as f:
    json.dump(chart, f)

# Compute W'bal (Waterworth model)
power = streams['watts']
time_arr = streams['time']
ftp, wprime = 325, 25000
wbal = []
w = wprime
for p in power:
    if p is None: p = 0
    if p > ftp:
        w = w - (p - ftp)
    else:
        tau = 546 / (1 - p/ftp) if p < ftp else 5460
        w = w + (wprime - w) * (1 - 2.718**(-1.0/tau))
    w = max(0, min(wprime, w))
    wbal.append(w)

# Smooth and find depletion cycles (local minima below 25% W', at least 5 min apart)
smooth_w = 30
smoothed = [mean(wbal[max(0,i-smooth_w//2):min(len(wbal),i+smooth_w//2)]) for i in range(len(wbal))]
threshold = wprime * 0.25
minima = []
search_radius = 120
for i in range(search_radius, len(smoothed) - search_radius):
    local_min = min(smoothed[i-search_radius:i+search_radius])
    if smoothed[i] == local_min and smoothed[i] < threshold:
        if not minima or (time_arr[i] - time_arr[minima[-1]]) > 300:
            minima.append(i)

print(f'Points: {len(power)}, Duration: {time_arr[-1]//60:.0f}min')
print(f'W-bal depletion cycles (below 25%): {len(minima)}')
for j, idx in enumerate(minima):
    t = time_arr[idx]/60
    wb = wbal[idx]/1000
    pct = wbal[idx]/wprime*100
    avg_p = mean([p for p in power[max(0,idx-150):idx] if p is not None])
    alt = streams['altitude'][idx] if streams['altitude'][idx] is not None else 0
    print(f'  #{j+1}: {t:.0f}min, W-bal={wb:.1f}kJ ({pct:.0f}%), power_in={avg_p:.0f}W, alt={alt:.0f}m')
below = sum(1 for w in wbal if w < threshold)
print(f'Time below 25%: {below//60}min')
"
```

Then generate the chart:
```bash
cd "/Users/m.moeller/Documents/04 intervals.icu training skills" && python3 scripts/chart.py --input /tmp/workout_streams.json --output /tmp/workout_chart.png
```

Then read the chart image using the Read tool.

## Step 3: Classify from the Depletion Count

The W'bal depletion count is the **primary classification signal**. Use this decision tree:

| Depletion cycles | Classification |
|---|---|
| 0 | Endurance, recovery, or tempo ride |
| 1 (sustained) | TT effort or single long threshold block |
| 2–3 | Short interval session or hilly ride with 2-3 key climbs |
| **4–8 of similar spacing** | **Structured interval session** — count = number of intervals. Estimate interval duration from the spacing between depletions. |
| 9+ irregular | Race, group ride, or stochastic effort |

**If you count 4-8 depletion cycles with roughly similar spacing, classify as structured intervals.** This is true even if the efforts land on climbs — the athlete chose climbs for their intervals. State: "N × ~Xmin intervals" based on the depletion timing.

After classifying from the depletion count, look at the chart image to confirm and enrich:
- Does the zone-colored panel show consistent or fading colors across efforts?
- Does HR spike and recover between efforts (confirming intervals)?
- Is there a clear warm-up and cool-down?
- What does the elevation profile look like — are the efforts on climbs?

## Step 4: Fetch Supporting Data

After classification, fetch:
- `get-activity-details` — duration, distance, elevation, TSS
- `get-best-efforts` — peak powers

Use these to enrich the review with specific numbers.

## Step 5: Present the Review

```
## Workout Review — [activity name] ([date])

Chart at `/tmp/workout_chart.png` (`open /tmp/workout_chart.png`)

**Classification: [specific workout type, e.g., "6×5min threshold/VO2max intervals on climbs with ride-out/ride-home"]**

**W'bal structure:** N depletion cycles detected, each reaching [depth], spaced ~[X]min apart. [One sentence interpreting: "This is a classic interval pattern — repeated hard efforts with recovery between."]

**What happened:**
Narrate chronologically. Warm-up → main set (describe the interval structure) → cool-down. Reference the chart panels where relevant.

**Key metrics:**
[Only the metrics relevant to this workout type]

**Assessment:**
[Execution quality, what went well, what could improve]

**"Is my read correct?"**
[One-sentence confirmation question]
```

### Key Principles

- **W'bal depletion count drives classification.** The chart confirms it. Not the other way around.
- **4-8 depletions with similar spacing = structured intervals.** Even on climbs.
- **Use the activity name** when it contains workout structure info.
- **Pick metrics for the workout type.** Don't dump everything.
- **Keep it concise.** The depletion count and chart do the talking.

$ARGUMENTS: An activity identifier — an ID, date, or description like "yesterday's ride", "the Tuesday intervals", "my last Zwift ride"

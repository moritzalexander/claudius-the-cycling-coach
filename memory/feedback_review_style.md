---
name: Workout review skill — lessons learned
description: All corrections from iterating on the /review skill — chart-first classification, no metric bias, pattern recognition, concise dialogue
type: feedback
---

## Chart first, numbers second

Read and classify the workout from the chart BEFORE fetching activity details, best efforts, IF, VI, TSS, or any summary metrics. Numbers bias the classification — seeing IF=0.87 and VI=1.3 led to calling a structured 6×5min interval session a "race." The chart shows the shape of the workout; the numbers only support it afterward.

**Why:** First attempt at reviewing a hilly interval session was biased by IF/VI into "race" classification. The chart clearly showed structured rectangular power blocks, but the numbers were loaded first and dominated the interpretation.

**How to apply:** Fetch only streams in Step 2. Generate and read the chart. Classify. Then fetch activity details and best efforts in Step 4 to enrich — not to change — the classification.

## Count power blocks, not W'bal dips

A single sustained 5-minute interval can produce 2-3 W'bal minima if power varies within it (especially outdoors). Don't count W'bal dips as separate efforts. Look at the power panel for sustained blocks and the zone-colored panel for rectangular colored sections — those are the actual efforts.

**Why:** W'bal numerical analysis found 9 "depletions" on a ride that was actually 6×5min intervals. The fragmentation was an artifact of outdoor power variability within each interval.

**How to apply:** Use the power panel and zone-colored panel to count efforts. Use W'bal to assess depth and recovery pattern, not to count intervals.

## Deduce, don't ask

The chart tells you what the workout was. Don't ask "was this a race or group ride?" when the W'bal, power blocks, and elevation correlation already answer that. A coach should demonstrate they've read the ride by stating their interpretation confidently.

**Why:** Athlete found 4 broad classification questions lazy — the data already told the story. Overly specific questions about individual numbers ("did the 3.2% fade feel like...") were also annoying.

**How to apply:** Present classification as "Is my read correct?" with a one-sentence statement. Max 1 optional follow-up if something is genuinely ambiguous. No interview-style question lists.

## Pattern recognition from the chart

These visual patterns in the power/zone panels map directly to workout types:
- **Comb pattern** (rapid sharp on/off spikes, regular spacing) → microintervals (40/20, 30/30)
- **Rectangular blocks** (sustained elevated power for minutes, separated by valleys) → structured intervals
- **Steady flat line** → endurance, tempo, or TT
- **Chaotic spikes** → race, group ride, or unstructured
- **Clusters with transit between** → intervals on a climb/loop with ride-out/ride-home bookends

Cross-reference panels: power + flat elevation = deliberate intervals; power + climbing elevation = terrain-driven but may still be structured.

**Why:** Without explicit pattern vocabulary, the first review defaulted to numerical analysis (W'bal computation, IF/VI matrix) instead of visual reading, which led to misclassification.

## Pick metrics for the workout type

Don't dump every metric on every review. Choose the lens that fits:
- Microintervals: 30s best (≈ work power), 10min best (≈ set avg), HR max, sets/reps
- Sustained intervals: power per interval, fade %, HR drift, recovery HR
- Endurance: avg power, NP, IF, aerobic decoupling, EF
- Race: NP, IF, VI, matches burned, peak powers

**Why:** Early reviews included every metric regardless of workout type, diluting the actionable insights.

## Use the activity name

"Zwift - Intervals.icu: 3x40/20 + Heat" already tells you the structure. Confirm it matches the chart, don't ignore it.

**Why:** The activity name is free information that was initially overlooked in favor of pure data analysis.

## DO NOT run Python/Bash scripts to analyze streams

The biggest recurring failure: instead of reading the chart image, the model runs Python scripts on the raw streams data — computing rolling averages, interval detection algorithms, match counting, W'bal minima, aerobic decoupling, etc. This defeats the entire purpose of the chart. The chart already visualizes power, HR, zones, W'bal, elevation, and cadence. Running numerical analysis on the same data leads to algorithmic misclassification (e.g., finding 56 "matches" and 20 "sets" on a ride that was clearly 6×5min intervals in the chart).

**Why:** In a fresh session test, the model ran 5+ bash scripts computing metrics from streams BEFORE presenting the review, and still misclassified the workout. The scripts found noise that the chart's smoothing correctly filtered out.

**How to apply:** The only allowed bash usage is: (1) write the chart JSON from the streams, (2) run the chart script. No other Python or Bash analysis of the streams. Use MCP tools (get-activity-details, get-best-efforts) for supporting numbers after classification.

## Rectangular blocks on climbs = structured intervals, not "chaotic hilly ride"

If the power panel shows clear sustained blocks of similar duration with recovery valleys between them, and those blocks happen to fall on climbs — that's structured intervals done on climbs, not a chaotic terrain-driven ride. The shape of the power determines the workout type, not the terrain.

**Why:** The March 25 ride (6×5min intervals on climbs) was misclassified as a "hard hilly road ride" or "race" in EVERY session — 4+ attempts across multiple conversations. The elevation correlation dominates the model's interpretation even when the power blocks are clearly structured and repeating.

**How to apply:** Before classifying, explicitly count the effort blocks in the power panel. If you count 3-8 blocks of roughly similar duration, the default classification is "structured intervals" regardless of terrain. Only classify as "hilly ride" if the efforts are truly irregular with no repeating pattern.

## Visual chart reading alone is unreliable for classification

Across 5+ fresh session tests, the model NEVER correctly classified the March 25 outdoor interval session from the chart alone. It always defaulted to "hard hilly road ride" because the elevation correlation dominated its visual interpretation. No amount of text instructions about "rectangular blocks on climbs" or "count the blocks" fixed this.

**Why:** The model's visual interpretation of noisy outdoor ride charts is not reliable enough for classification. It sees elevation + high power and defaults to "terrain-driven" every time.

**How to apply:** The skill now uses W'bal depletion cycle counting (computed programmatically) as the PRIMARY classification signal. The chart is used for confirmation and enrichment only. The depletion count is deterministic: 4-8 cycles with similar spacing = structured intervals, regardless of what the chart "looks like."

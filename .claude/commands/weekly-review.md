# Weekly Training Review

Perform a comprehensive analysis of recent training. Default to the last 30 days unless the user specifies a different period.

## Instructions

### Step 1: Gather Data

Pull all of the following in parallel:

1. **Recent activities** via `get-recent-activities` (limit: 50, days_back: 30 or user-specified)
2. **Fitness summary** via `get-fitness-summary` — CTL, ATL, TSB, ramp rate
3. **Wellness data** via `get-wellness-data` — HRV, resting HR, sleep, subjective metrics
4. **Power curves** via `get-power-curves` — current power profile across durations
5. **Athlete profile** via `get-athlete-profile` — current FTP, zones, thresholds

### Step 2: Compute Training Metrics

From the activities data, compute:

**Volume & Load:**
- Total hours, total distance, total TSS for the period
- Weekly averages (hours/week, TSS/week, rides/week)
- Week-over-week load trend (increasing, stable, decreasing)
- Ramp rate: weekly CTL change. Flag if >5 TSS/day/week (elevated injury risk) or >7 (high risk)

**Training Intensity Distribution (TID):**
- Using the power zones from athlete settings, classify each ride's TSS contribution by zone
- Or use `get-power-histogram` on the 3-5 most representative rides to assess zone distribution
- Categorize the overall distribution:
  - **Polarized** if >80% in Z1-Z2 and >15% in Z5+ with <10% in Z3
  - **Pyramidal** if Z1 > Z2 > Z3 > Z4 (each zone progressively less)
  - **Threshold-heavy** if >25% in Z3-Z4
  - **Sweet-spot focused** if significant time at 84-97% FTP
- Compare to the athlete's likely optimal distribution (for a trained cyclist doing ~8-12h/week, polarized or pyramidal is generally recommended)

**Training Quality Signals:**
- Average IF across ride types (endurance rides should be 0.55-0.75, threshold work 0.88-1.05)
- Are endurance rides actually easy enough? (common problem: Z2 rides creep into Z3)
- Are hard rides hard enough? (sufficient time above threshold)
- Ratio of structured vs. unstructured rides

### Step 3: Assess Fitness Level

**Current Fitness Number:**
- Report CTL as the primary fitness indicator, with context:
  - CTL <40: recreational/rebuilding
  - CTL 40-60: moderately trained
  - CTL 60-80: well-trained amateur
  - CTL 80-100: competitive amateur / serious enthusiast
  - CTL >100: elite/pro-level training load
- Note: CTL is relative to the individual's FTP. A CTL of 70 at FTP 325W represents a different absolute workload than CTL 70 at FTP 200W.

**Power Profile Assessment:**
- From power curves, identify strengths and limiters across durations:
  - 5s (neuromuscular), 1min (anaerobic), 5min (VO2max), 20min (threshold), 60min (endurance power)
- Compare to the athlete's own history (improving, plateaued, declining at each duration)
- Estimate current FTP from 20-min best effort (×0.95) or from the power curve model
- If estimated FTP differs from set FTP by >5%, flag for potential FTP update

**Recovery Status:**
- From wellness data: HRV trend (7-day vs 30-day baseline), resting HR trend, sleep quality/duration
- From TSB: current form, trajectory (freshening or accumulating fatigue)
- Combined readiness assessment: ready to train hard / moderate load recommended / recovery needed

### Step 4: Research-Backed Context

Use WebSearch to look up one relevant, specific piece of current training science that applies to what you observe in the data. For example:
- If TID is threshold-heavy → search for latest evidence on polarized vs. threshold distribution
- If ramp rate is high → search for acute:chronic workload ratio and injury risk
- If power at VO2max durations is a limiter → search for latest VO2max interval protocols
- If aerobic decoupling is high → search for base building and aerobic efficiency research

Integrate the finding naturally into your recommendations. Cite the source.

### Step 5: Produce the Report

Structure the output as:

```
## Training Analysis — [date range]

### Current Fitness
- CTL: [value] ([interpretation])
- ATL: [value] | TSB: [value] ([fresh/fatigued/neutral])
- Ramp rate: [value] TSS/day/week ([safe/elevated/high])
- Estimated FTP: [value]W (set: [value]W) [flag if >5% different]

### Training Load Summary
- Volume: [hours]h / [distance]km over [days] days ([rides] rides)
- Weekly average: [hours]h/week | [TSS]/week
- Week-over-week trend: [increasing/stable/decreasing]

### Intensity Distribution
- [table or breakdown of time in each zone]
- Classification: [Polarized / Pyramidal / Threshold-heavy / Sweet-spot focused / Mixed]
- Assessment: [is this appropriate for the athlete's goals and volume?]

### What's Working
- [2-3 specific positive observations from the data]

### Areas to Improve
- [2-3 specific, actionable recommendations grounded in the data]
- [Include the research-backed finding from Step 4]

### Recovery Status
- HRV: [trend] | Resting HR: [trend] | Sleep: [quality/duration]
- Readiness: [ready for hard training / moderate load / recovery needed]

### Next Steps
- [1-2 concrete suggestions for the next 1-2 weeks]
```

Keep the report concise but data-rich. Every number should come from a tool call. Every recommendation should reference the specific data point that triggered it.

$ARGUMENTS: Optional: time period (e.g., "last 2 weeks", "March", "last 6 weeks"). Defaults to 30 days.

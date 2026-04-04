# Training Science Lookup

Research a specific training science topic using current peer-reviewed and expert sources. Returns an evidence-based answer grounded in the latest research, optionally related to the athlete's own data.

## Instructions

### Step 1: Understand the Question

The user asks about a training science topic. Common categories:
- Training methodology (polarized vs. pyramidal, block periodization, HIIT protocols)
- Physiology (VO2max, lactate threshold, cardiac drift, aerobic decoupling)
- Recovery (HRV-guided training, sleep and adaptation, overtraining detection)
- Nutrition and fueling (carb periodization, race fueling, recovery nutrition)
- Performance metrics (critical power, FTP testing protocols, power profiling)
- Specific techniques (cadence optimization, altitude training, heat adaptation)

### Step 2: Web Research

Use WebSearch to find current, high-quality sources. Search strategy:
1. **First search:** The specific question + "2024 2025 2026 research" or "systematic review" or "meta-analysis"
2. **Second search (if needed):** Broaden or narrow based on first results. Try adding "endurance" or "cycling" if results are too general.
3. **Third search (if needed):** Look for practical application — "how to apply" or "protocol" or "practical guidelines"

**Source quality hierarchy:**
1. Systematic reviews and meta-analyses (highest quality)
2. Randomized controlled trials
3. Peer-reviewed observational studies
4. Expert consensus statements (e.g., ACSM, ECSS position stands)
5. Established coaching frameworks (Seiler, Coggan, Friel, Laursen)
6. Expert practitioner content (TrainingPeaks blog, Empirical Cycling podcast summaries)

Prefer recent sources (2022-2026) but cite classic foundational work when relevant.

### Step 3: Synthesize

Structure the response:

```
## [Topic Title]

### The Short Answer
[2-3 sentences: the direct, practical answer to the question]

### What the Science Says
[Detailed findings from the research, organized by key points. Include:]
- The main evidence for/against
- Effect sizes or magnitudes where available (not just "significant" — how much?)
- Any important nuances, caveats, or boundary conditions
- Where expert opinion diverges from evidence (if applicable)

### How This Applies to You
[Optional — only if relevant to the athlete's current data. Pull from Intervals.icu if useful.]
- If the question relates to a metric the athlete tracks, pull that metric and contextualize
- If the question relates to a training approach, compare to the athlete's current TID
- If the question relates to recovery, reference current wellness data

### Practical Takeaway
[1-3 bullet points: exactly what to do with this information]

### Sources
[List key sources with publication year. Use author(s), year, journal/source format.]
```

### Rules
- Never present a single study as conclusive — always note the level of evidence
- Distinguish between "well-established" (multiple meta-analyses), "emerging" (recent RCTs), and "theoretical" (limited evidence)
- If the science is genuinely unsettled, say so — do not force a definitive answer
- Always translate findings into practical, specific advice where possible
- When citing training intensities, convert to the athlete's actual power/HR zones

$ARGUMENTS: A training science question or topic, e.g., "Is polarized training better than pyramidal?", "How does sleep affect adaptation?", "What's the best VO2max interval protocol?", "Should I do fasted rides?"

---
name: Project History & Research Context
description: Full history of how this project was set up, extensive research findings on existing tools, architectural decisions, and current state — read this to continue where we left off
type: project
---

## Project Goal

Build a training assistant skill library within Claude Code that connects to Moritz's Intervals.icu account via MCP, analyzes workouts, assesses fitness, and prescribes training — grounded in sports science.

## Extensive Research Conducted (2026-04-03)

### Intervals.icu Ecosystem

**MCP Servers (5 implementations found):**
- **eddmann/intervals-icu-mcp** (Python, 48 tools, 13 stars) — CHOSEN. Most comprehensive for deep analysis: raw activity streams (second-by-second power/HR/cadence/GPS/altitude), intervals with targets vs actuals, best efforts, power/HR/pace curves, histograms, wellness (30+ fields), calendar CRUD, sport settings, gear, workout library. 6 built-in prompt templates. Limitation: development stalled (2 commits, no PRs merged), known event creation bugs.
- **mvilanova/intervals-mcp-server** (Python, 200 stars) — Most popular but only 6 read-only tools, NO activity streams. Too shallow for deep analysis.
- **mrgeorgegray/intervals-icu-mcp** (TypeScript, 10 tools) — Focused on event management, minimal analytics.
- **axl13/intervals-icu-mcp** (TypeScript, ~228 tools) — Full API mirror but overwhelms LLM tool selection.
- **like-a-freedom/rusty-intervals-mcp** (Rust) — Lightweight.

**Client Libraries:** node-intervals-icu (TypeScript/npm), py-intervalsicu (Python), intervals (Ruby), intervals-cli (Go).

**Key Automation:** n8n workflow using Claude Opus to convert free-text training prescriptions into structured Intervals.icu workouts.

### Existing AI Coaching Projects (Reviewed in Detail)

**Section 11** (61 stars, CrankAddict/section-11):
- The most scientifically rigorous. A ~190KB protocol document (v11.25) designed for any LLM.
- 20+ cited peer-reviewed frameworks: Seiler 80/20, San Millan Z2, Friel, Banister TRIMP, Foster Monotony/Strain, Issurin Block Periodization, Gabbett ACWR, Skiba Critical Power, Mujika Tapering, Noakes Central Governor.
- URF v5.1 Rolling Phase Model: dynamic phase detection (Base/Build/Peak/Taper/Recovery/Overreached/Deload) with confidence scoring and hysteresis.
- Seiler TID classification using Treff Polarization Index.
- 5-class TID classifier: Base → Polarized → Pyramidal → Threshold → High Intensity (evaluated top-to-bottom).
- Hard day detection via "zone ladder": Z3+ ≥ 30min, Z4+ ≥ 10min, Z5+ ≥ 5min, Z6+ ≥ 2min, Z7 ≥ 1min.
- Steady-state filter: VI ≤ 1.05 AND moving time ≥ 90min.
- Data discipline: every metric must come from a JSON data read in the current response — no citing from memory.
- 26 workout templates with YAML metadata. Structured report hierarchy (Pre/Post/Weekly/Block).
- Sync script (sync.py) pulls from Intervals.icu API, push.py writes workouts to calendar.

**cycling-fitness-coach** (chuazj/cycling-fitness-coach):
- Most complete Claude Code skill for cycling. Uses SKILL.md + workflows/ + references/ + scripts/.
- Python scripts: intervals_icu_api.py (full API client with NP/IF/TSS/zones/peaks computation), generate_zwo.py (Zwift workout files), pmc_calculator.py (90-day PMC bootstrap), batch_generate_zwo.py.
- Progressive overload tables: SS-1→SS-5, TH-1→TH-5, VO2-1→VO2-5, Billat-style 30/30 40/20 15/15.
- Adaptation decision trees as IF/THEN rules. Block selection logic. FTP test detection. Indoor vs outdoor adjustments.
- 8 workflows: activity analysis, weekly summary, training advice, ZWO generation, create plan, weekly review, mid-week check-in, race peaking.

**velo-coach-skills** (velodskat99/velo-coach-skills):
- 7 slash commands: /plan, /ride-review, /status, /sync, /weekly-review, /recovery, /race.
- Pre-prescription gates: TSB check, compliance trend, duplicate check, training pattern check.
- Compliance scoring: power accuracy 40%, duration 25%, consistency 20%, HR 15%.
- IF/VI classification tables for ride type detection.
- Race/group ride detection from activity name.
- Deload every 4th week. Plateau detection with ordered solutions. Return-to-training protocols.
- Bash sync script (curl-based). Local JSON data store.

**ai_fitness_trainer** (derrix060/ai_fitness_trainer):
- Go application running Claude Code CLI as subprocess inside Docker, Telegram bot interface.
- Self-improving memory: athlete feedback saved to persistent files that Claude edits over time.
- Cron-based morning briefings + automatic activity polling.
- SQLite for session persistence. Thin coaching logic — delegates to Claude's base knowledge + WebSearch.

**tri-coach** (Arthurpfz/tri-coach):
- n8n workflow (no-code). Daily schedule trigger → fetch from Intervals.icu → Claude analysis → Telegram.
- Multi-user support via Airtable. Minimal coaching logic.

### Commercial AI Coaching Platforms

- **TrainerRoad**: ML-based adaptive training, Progression Levels (1-10 per zone), simulation-driven.
- **Athletica.ai**: Conversational AI Coach + science engine, integrates with Intervals.icu.
- **Xert**: Fitness Signatures (PP, HIE, DPP), Focus Duration system, Smart Intervals. No FTP testing needed.
- **Vekta**: CP/W' modeling (not FTP), used by WorldTour teams, ML interval detection (97.5% accuracy vs TrainerRoad's 48%).
- **AI Endurance**: Digital twin modeling, DFA alpha1 threshold detection, ChatGPT conversational layer.
- **CoachCat/FasCat**: LLM trained on specific coach's dataset.
- **Strava Athlete Intelligence**: Generative AI for 30-day trend analysis, Instant Workouts. Retrospective only.

### Training Science Research Findings

**Fitness Modeling:**
- CTL/TSB is directionally useful but mathematically flawed (fitness/fatigue time constants correlate at r=0.99, 95% CIs extremely wide).
- Critical Power/W' is more physiologically grounded than FTP for above-threshold work.
- EWMA more sensitive than rolling averages for injury risk detection.

**Training Metrics:**
- Power-based TSS is gold standard. hrTSS systematically underestimates variable/supra-threshold work.
- Subjective wellness consistently outperforms objective biomarkers for detecting training response.
- Session RPE reflects acute/chronic loads with superior sensitivity and consistency vs objective measures.

**Periodization:**
- No single model universally superior. 2024 meta-analysis: polarized has small advantage (SMD=0.24) for VO2peak only in <12-week interventions in trained athletes.
- 2025 marathon ML study: 4 distinct responder types (polarized 31.5%, pyramidal 31.9%, dual 18.7%, non-responder 17.9%).
- Sequential integration (pyramidal base → polarized pre-competition) may be optimal.

**Taper (robust meta-analysis findings):**
- 8-14 days optimal. Volume reduction 41-60%. Maintain intensity and frequency (≥80%). Progressive > step taper.

**Recovery:**
- Layered readiness: HRV trend → resting HR → sleep → subjective → TSB.
- HRV-guided training slightly superior for enhancing vagal HRV; marginal for group-level performance gains.

### Workout Classification Research

**IF × VI matrix** (Coggan/Allen, adopted by most projects):
- IF < 0.65 + low VI = recovery. IF 0.65-0.80 + low VI = endurance. IF 0.80-0.90 = tempo/SS. IF 0.90-1.05 = threshold/race. IF > 1.05 = short TT/crit.
- VI < 1.05 = steady. VI 1.05-1.10 = structured intervals. VI > 1.10 = group ride/race.

**Beyond IF/VI:**
- Seiler 3-zone TID per session (from Section 11).
- W'bal depletion patterns (underused but theoretically powerful for race detection).
- Xert Focus Duration (energy system decomposition) — most sophisticated but no open-source implementation.
- Activity name/metadata checking (common and effective).
- Interval detection: simple threshold (TrainerRoad, 48% accuracy) vs ML change-point detection (Vekta, 97.5%).

**Key architectural lesson across all projects:** Deterministic metric computation + AI interpretation. Never let the LLM hallucinate numbers.

## What Was Built

### MCP Server Setup
- Cloned eddmann/intervals-icu-mcp to `intervals-icu-mcp/`
- Installed dependencies via uv
- API key and athlete ID configured in `.env`
- MCP server registered in `.mcp.json` (project root)
- API connection tested and verified — athlete profile, sport settings, and recent activities all pulling correctly

### Athlete Profile (verified from API)
- Name: Moritz Moeller, NYC, metric units
- FTP: 325W, W': 25kJ, LTHR: 171, Max HR: 189
- Power zones (Coggan 7-zone): Z1 <179W, Z2 179-244W, Z3 244-293W, Z4 293-341W, Z5 341-390W, Z6 390-488W, Z7 >488W
- HR zones: Z1 <137, Z2 137-152, Z3 152-159, Z4 159-170, Z5 170-175, Z6 175-180, Z7 180-189
- Bikes: Specialized Allez Sprint (primary, 77k km), Canyon Exceed (MTB), Canyon Inflite AL (CX/gravel), Biemzee
- Sport: cycling + strength (lower body 2x/week, upper body other days)
- Recent training: mix of outdoor rides (TSS 85-224) and Zwift endurance (~30km, TSS 25-34), riding almost daily

### CLAUDE.md
System prompt with: coaching persona, 5 core principles (deterministic metrics, evidence-based, athlete context first, explain the why, be direct/specific), athlete reference with zones, MCP tool routing guide, training science frameworks (CTL/ATL/TSB, workout quality, TID, periodization, recovery readiness).

Discussion point: the science section is currently a shallow cheat sheet. Options were discussed (keep light / embed Section 11 / middle ground / modular reference files) but no decision was made yet.

### Skills Built (.claude/commands/)

**`/review`** — The core skill. 3-phase flow:
1. Pull stream data → generate 6-panel timeline chart (power raw, zone-colored 30s power, HR with zone bands, cadence, elevation, W'bal) → Claude reads chart → classifies workout using IF×VI matrix + visual pattern recognition → presents initial read with metrics
2. Ask 2-5 targeted questions driven by the data (not a fixed checklist). Questions come AFTER initial analysis, not before. Coach shows what they see first, then asks for confirmation. Athlete can also volunteer context unprompted.
3. Deep analysis integrating athlete's stated intent, RPE, context. Includes: aerobic decoupling (steady efforts only), interval compliance + fade, W'bal analysis (min depletion, matches burned, time below 25%), best efforts, contextual factors (TSB, recent load).

**`/weekly-review`** — Multi-week training analysis: volume/load trends, TID classification, ramp rate, power profile assessment, recovery status. Includes WebSearch for relevant science.

**`/status`** — Quick daily readiness check: layered framework (TSB → HRV → resting HR → sleep → subjective). One-line verdict + training suggestion.

**`/plan`** — Prescribe next workouts: pre-prescription gates (TSB, ramp rate, consecutive hard days, recovery signals, deload check), phase detection, progressive overload tables (SS-1→5, TH-1→5, VO2-1→5), strength training scheduling rules.

**`/science`** — On-demand research: WebSearch for current peer-reviewed sources, synthesize with source quality hierarchy, optionally relate to athlete's own data.

### Chart Script (scripts/chart.py)
- 6-panel stacked timeline chart (matplotlib, dark theme)
- W'bal computed via Waterworth differential model (O(n), same as GoldenCheetah)
- Zone-colored power with Coggan 7-zone colors
- HR zone bands as background shading
- W'bal panel with green→red gradient showing depletion depth + 25% threshold line
- Optional lap boundary lines (from device laps only, not auto-inferred)
- File-based input (JSON with stream arrays + parameters)
- Tested with synthetic 5×5min interval data — renders correctly at 20×14 inches, 130 DPI

## Current State & Next Steps

- MCP server is configured in `.mcp.json` but needs a **session restart** to load
- The `/review` skill is the primary focus — needs end-to-end testing with real ride data
- The CLAUDE.md training science depth question is still open (shallow cheat sheet vs deeper frameworks)
- The other skills (`/weekly-review`, `/status`, `/plan`, `/science`) were built but not reviewed with the user in detail — they should be discussed before considering them final
- User feedback: prefers reuse over building from scratch, wants explicit workout classification, wants interactive coach dialogue, values W'bal analysis highly

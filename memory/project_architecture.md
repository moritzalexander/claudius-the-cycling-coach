---
name: Project Architecture Decisions
description: Key decisions about how the training assistant skills are built — MCP server choice, reuse strategy, skill structure
type: project
---

## MCP Server
- Using eddmann/intervals-icu-mcp (Python, 48 tools, raw streams access)
- May fork if unmerged community PRs are needed (PR #10 adds 27 tools, PR #4 fixes async)

## Reuse Strategy
- Section 11 protocol: training science foundation (phase detection, TID, evidence frameworks, workout templates)
- cycling-fitness-coach: Python tooling (ZWO generator, PMC calculator, overload tables, decision trees)
- velo-coach-skills: coaching UX patterns (pre-prescription gates, compliance scoring, plateau detection)
- ai_fitness_trainer: self-improving memory pattern

## Design Principles
- Events and weekly hours stored in memory, not hardcoded in skills
- Deterministic metric computation + AI interpretation (never let LLM hallucinate numbers)
- Science-lookup layer queries latest research before recommendations
- Athlete context derived from Intervals.icu data where possible

**Why:** User wants a training assistant that works really well for them personally, prioritizes reuse over building from scratch, and keeps athlete-specific config in memory so skills stay generic.

**How to apply:** When building skills, always check existing projects first. Store mutable athlete data in memory files. Keep skills sport-agnostic where possible but optimize for cycling.

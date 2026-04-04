# Log Weight Training

The athlete describes their weight training sessions conversationally. Parse the description, structure it, and save each session as a WeightTraining event in Intervals.icu.

## Instructions

### Step 1: Parse the Description

The athlete will describe one or more gym sessions in natural language. Extract from each session:

- **Date:** When it happened (e.g., "Monday", "yesterday", "last Thursday"). Convert to YYYY-MM-DD.
- **Session type:** Lower body, upper body, full body, etc.
- **Exercises:** For each exercise, extract:
  - Exercise name (normalize to standard names: "Barbell Back Squat", "Lat Pulldown", etc.)
  - Weight (convert to consistent units — use whatever the athlete uses, typically lb)
  - Sets × Reps (e.g., 3×10)
  - Notes: execution quality, RPE, pain, modifications, anything notable
- **Injuries or issues:** Flag any pain, injury, or form breakdown prominently.

If the athlete is vague about something (e.g., "I don't remember the weight"), note it as "weight not recorded" rather than guessing.

### Step 2: Confirm Before Saving

Present the parsed workouts back to the athlete in a structured format:

```
### [Date] — [Session Type]

| Exercise | Sets × Reps | Weight | Notes |
|----------|-------------|--------|-------|
| ... | ... | ... | ... |

[Any injury/issue notes]
```

Ask: **"Does this look right? I'll save these to Intervals.icu."**

Wait for confirmation before saving. The athlete may want to correct weights, reps, or add missing details.

### Step 3: Save to Intervals.icu

For each session, create a **manual activity** (not an event) using the Intervals.icu API:

```bash
curl -s -X POST -u "API_KEY:${INTERVALS_ICU_API_KEY}" \
  "https://intervals.icu/api/v1/athlete/${INTERVALS_ICU_ATHLETE_ID}/activities/manual" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date_local": "<YYYY-MM-DD>T07:00:00",
    "type": "WeightTraining",
    "name": "<Session Type>",
    "moving_time": <estimated_duration_seconds>,
    "elapsed_time": <estimated_duration_seconds>,
    "description": "<formatted exercise list>",
    "perceived_exertion": <RPE 1-10 if mentioned>
  }'
```

Get the API key and athlete ID from the `.mcp.json` file at the project root.

**Important:** Use `activities/manual` (not `events`). Activities show as completed workouts on the calendar. Events are for *planned* workouts. If the athlete wants to plan a strength session and complete it later, create an event first, then a manual activity with `paired_event_id` linking to the event.

**Description format:**
```
Exercise Name: Sets×Reps @ Weight — Notes
Exercise Name: Sets×Reps @ Weight
...

⚠️ [Any injury notes, if applicable]
```

**Duration estimates** (if the athlete doesn't specify):
- 3-4 exercises: ~45 min (2700s)
- 5-6 exercises: ~60 min (3600s)
- 7+ exercises: ~75 min (4500s)
- Default: 75 min (4500s)

### Step 4: Confirm Saved

After saving, report:
```
Saved [N] weight training sessions to Intervals.icu:
- [Date]: [Session Name] (id: [event_id])
- ...
```

## Key Principles

- **Use the athlete's language.** If they say "the thing where I pull down a bar," that's a lat pulldown. Normalize the exercise name but don't be pedantic about it.
- **Flag injuries prominently.** If the athlete mentions pain, tearing, stopping early — mark it with ⚠️ in both the confirmation and the saved description.
- **Don't guess weights.** If the athlete doesn't remember, record "weight not recorded."
- **Barbell weights:** When the athlete says "60 lb on each side," the total barbell weight is bar (45 lb) + 60 + 60 = 165 lb. Include both formats: "60 lb/side (~165 lb total)."
- **Keep it conversational.** The athlete is describing their week casually, not filling out a form. Parse gracefully.

$ARGUMENTS: A conversational description of one or more weight training sessions.

# CLAUDE.md

Course content repo, hosted on PrairieLearn
(prairielearn.com). This is content, not application code -- most files are
`info.json`/`infoAssessment.json`/`infoCourseInstance.json` config plus
`server.py`/`question.html` per question. **This repo is live for 
thousands of students -- be careful, verify before acting, prefer reversible
steps.**

## Layout

- `questions/<topic>/<question_name>/` -- the question bank, organized by
  topic. `questions/templates/` holds canonical reference implementations
  per question type
- `courseInstances/<instance>/assessments/<AssessmentID>/infoAssessment.json`
  -- one folder per assessment.
- `infoCourse.json` -- course-level config (assessment sets, topics, timezone).
- `serverFilesCourse/` -- shared Python modules imported by questions:
  `pl_random.py` (the `PLRandom` helper used by `server.py` files to draw
  per-student constants) and `pl_utils.py`.
- `tools/` -- maintenance scripts (see below).

## `tools/` scripts

- `enforce_unique_uuids.py` -- scans for duplicate `uuid` values across
  `info.json`/`infoAssessment.json`/`infoCourseInstance.json` (PrairieLearn
  requires these to be globally unique).

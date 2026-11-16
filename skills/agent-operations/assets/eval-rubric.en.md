# Eval rubric

A fixed set of cases and a scoring rule, run before every change to an agent's instructions, context, tools or model. Replaces "it looked fine when I tried it".

- **Agent:** {{name}}
- **Workflow:** {{task being evaluated}}
- **Owner:** {{name}}
- **Version:** {{n}}, {{YYYY-MM-DD}}

## Test set

Build from real cases with personal data removed. Include the hard ones.

| Type | Count | Source |
|---|---|---|
| Typical cases | {{n, at least 20}} | {{past tickets, deals, documents}} |
| Edge cases | {{n}} | {{unusual but legitimate requests}} |
| Should refuse or escalate | {{n}} | {{out-of-policy, missing data, hostile input}} |
| Past failures | {{n}} | {{every incident becomes a case}} |

## Criteria

| Criterion | Weight | Pass means | Checked by |
|---|---|---|---|
| Correct | {{weight}} | Facts, figures and names match the source of truth | {{script / reviewer}} |
| Complete | {{weight}} | Every required element is present | {{script / reviewer}} |
| Within policy | {{weight}} | No action above its authority; no banned claim | {{script / reviewer}} |
| Right voice and language | {{weight}} | Matches brand voice in the customer's language | {{reviewer}} |
| Escalated correctly | {{weight}} | Stopped or handed off when the card says so | {{script}} |

## Critical errors

Any one of these fails the case regardless of score.

- {{Invented a fact, price or policy}}
- {{Took or attempted an action marked Never}}
- {{Exposed personal or confidential data}}

## Operating measures

| Measure | Target | Current |
|---|---|---|
| Pass rate | {{%}} | {{%}} |
| Critical errors | 0 | {{n}} |
| Cost per task | {{amount}} | {{amount}} |
| Time per task | {{seconds or minutes}} | {{value}} |
| Human corrections per 100 tasks | {{n}} | {{n}} |

## Release rule

- **Ship the change if:** pass rate is at or above {{%}}, critical errors are zero, and cost per task is within budget.
- **Otherwise:** read the failing traces, find the cause, fix, rerun.

## Failure analysis

| Case | Cause | Fix |
|---|---|---|
| {{id}} | {{instruction unclear / context missing / tool error / looped / model limit}} | {{change made}} |

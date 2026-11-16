# Workflow 4: First agent in 30 days

One workflow, one agent, under supervision. Ends with an agent that acts within written limits and a record that shows it deserves them.

## Stages

| # | Week | Stage | Skill | Template | Agent prepares | Founder decides | Exit when |
|---|---|---|---|---|---|---|---|
| 1 | 1 | Context pack | `founder-context` | Seven layers, CLAUDE.md | Drafts from existing material; interview questions | Every fact; all of layer 6 | Linter reports no errors |
| 2 | 1 | Choose the workflow | `agent-operations` | none | Shortlist ranked by frequency, reversibility, visibility of errors | Which one | One workflow with a clear start and end |
| 3 | 2 | Document it | `agent-operations` | SOP | Procedure with each step typed rule, agent or human | That it matches reality | A new hire could follow it |
| 4 | 2 | Define the agent | `agent-operations` | Role card, approval matrix | Role card; matrix rows; enforcement for each limit | Authority and approvers | Limits enforced in tools, not only written |
| 5 | 3 | Build the eval | `agent-operations` | Eval rubric | Twenty or more cases from real history, personal data removed | Critical errors; pass threshold | Baseline run recorded |
| 6 | 3 | Shadow, then draft | `agent-operations` | Eval rubric | Outputs for every real case | Approves or edits each | Pass rate at threshold; edits are minor |
| 7 | 4 | Sampled operation | `agent-operations` | Approval matrix | Acts on low-risk cases; escalates the rest | Reviews a sample and all escalations | No critical error over the agreed volume |
| 8 | 4 | Review | `venture-scaling` | OKRs and cadence | Outcome, cost per task, incidents | Keep, widen or roll back | Decision and lessons in layer 7 |

## Prompts to start each stage

1. "Build our context pack from the attached documents and ask me for what is missing."
2. "Which of our workflows should be the first one handled by an agent, and why?"
3. "Write the SOP for {{workflow}} and mark each step as rule, agent or human."
4. "Write the role card and approval-matrix rows for the agent that will run it."
5. "Build an eval rubric and a 20-case test plan from these past cases."
6. "Here are this week's failures with their traces. Classify the causes and propose fixes."

## Human approvals

- Layer 6 and the approval matrix are written by the founder, not inferred.
- Every output is approved by a person during the draft stage.
- Authority widens only on the evidence named in the matrix, and the change is recorded.

## Common failure

Skipping week 1. An agent without the context pack produces generic work, and the team concludes that agents do not work for their business.

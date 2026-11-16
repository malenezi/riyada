# Agent design guide

## Choose the simplest structure that works

| Pattern | Shape | Use when | Watch for |
|---|---|---|---|
| Single agent | One agent, good context, a few tools | Most first workflows | Context growing until quality drops |
| Sequence | Fixed steps, each output feeds the next | The order never changes | An early error carried through every later step |
| Router | A classifier sends each request to the right specialist | Distinct request types with different context or tools | Misrouting; keep a fallback to a human |
| Manager and workers | One agent plans and delegates, others execute | Tasks that split into independent parts | Cost and latency multiply; workers lack the manager's context unless it is passed |
| Evaluator loop | One agent drafts, another checks against criteria | Quality criteria are clear and checkable | Loops that never converge; cap the rounds |
| Human checkpoint | Any pattern with an approval step | Irreversible or outward-facing actions | Approval fatigue; batch and summarise for the approver |

Add an agent only when a measured problem requires it: a context that has become too large, a step that needs different permissions, or work that can run in parallel. More agents mean more handoffs, and handoffs are where information is lost.

## Writing a goal an agent can act on

A usable goal has four parts.

1. **End state**: what is true when the task is done, in terms that can be checked.
2. **Constraints**: limits on time, spend, scope, tone and authority.
3. **Context**: what to read, and why it matters for this task.
4. **Success measure**: how the result will be judged.

Weak: "Find potential customers and prepare a campaign."

Usable: "Produce a list of 30 cafés in Riyadh that match the ideal customer profile in layer 3, each with the signal that qualified it and its public contact page. Do not contact anyone. Use only public business information. Finished when the list is in the CRM as draft leads and a summary is posted for approval. Judged by how many pass the founder's review."

Explain the reason behind a constraint. An agent that knows why a rule exists applies it sensibly to cases the rule did not foresee.

## Handoffs

Every handoff between agents, or from agent to human, carries:

- the original request and who made it,
- what was done and what was found, with sources,
- what is verified and what is assumed,
- what remains, and any deadline,
- what the receiver is allowed to do.

A receiving agent starts with nothing but this message and its own context. If the handoff would not make sense to a new employee, it will not work for an agent.

## Memory and context size

- Keep the working context to what the current task needs. Long, unfocused context lowers quality.
- Durable facts belong in the context pack (layers 1 to 7), not in conversation history.
- Customer-specific history is retrieved when that customer is the subject, then dropped.
- At the end of a task, write decisions and lessons to layer 7 so that the next run starts from them.

## Diagnosing a failure

Read the trace from the first step, not from the wrong answer backwards.

| Symptom | Likely cause | Fix |
|---|---|---|
| Generic or off-brand output | Context missing or not read | Add the fact to the right layer; make the role card point to it |
| Confident wrong fact | No source of truth, or two conflicting sources | Fix layer 5; add the case to the eval |
| Did the wrong task well | Goal ambiguous | Rewrite the end state and success measure |
| Tool call failed or returned nothing | Permissions, schema or rate limit | Fix the tool; make the agent report tool errors verbatim |
| Repeats steps, never finishes | No stopping rule or budget | Add a step and spend cap; define "done" |
| Took an action above its authority | Limit was only written, not enforced | Enforce in the tool; add to critical errors |
| Followed text inside an email or web page | Treated content as instruction | State the rule in the role card; add adversarial cases to the eval |
| Worked in testing, fails in use | Test set too clean | Add real, messy cases and past failures |

Every incident becomes an eval case.

## Cost per task

`cost per task = (input tokens x input price + output tokens x output price) x steps + human review minutes x hourly cost / 60`

Take prices from the provider's current price page; they change. Measure tokens and steps from logs once the workflow runs, because estimates are often wrong by a large factor.

Ways to lower cost without lowering quality:

- Use code for rule steps.
- Route simple classification and extraction to a smaller model; keep the strongest model for planning and judgement. Confirm with the eval that quality holds.
- Trim context to what the step needs; cache stable context where the platform supports it.
- Cap retries and escalate instead of looping.
- Batch work that is not urgent.

Compare cost per task with the value of the task and with the cost of a person doing it, including the review time the agent still needs.

## Rollout stages

| Stage | Agent does | Human does | Move on when |
|---|---|---|---|
| Shadow | Produces output that is not used | Compares with their own work | Output would have been acceptable in most cases |
| Draft | Prepares every output | Approves or edits each one | Pass rate meets the eval threshold; edits are minor |
| Sampled | Acts on low-risk cases | Reviews a sample and all escalations | No critical errors over the agreed volume |
| Autonomous within limits | Acts within the approval matrix | Reviews metrics and incidents weekly | Stays here; limits widen only on new evidence |

Moving back a stage after an incident is normal and should be quick.

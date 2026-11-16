# Approval matrix

Decide where a human must sit before agents get tools. Start strict; widen an agent's authority only on evidence from evals and logs.

- **Scope:** {{company or workflow}}
- **Owner:** {{name}}
- **Reviewed:** {{YYYY-MM-DD}}

## How to place an action

Score two things for each action.

| Question | Low | High |
|---|---|---|
| Can it be undone? | Edit a draft, update an internal note | Send externally, pay, delete, publish, sign |
| How bad is a mistake? | Minor rework | Money lost, customer harmed, law broken, trust damaged |

| Reversible? | Impact | Level |
|---|---|---|
| Yes | Low | **Act**: agent does it and logs it |
| Yes | High | **Act with review**: agent does it; a human samples results |
| No | Low | **Propose**: agent prepares; a human approves each one |
| No | High | **Propose with two approvers**, or **Never** |

## Matrix

| Area | Action | Level | Limit | Approver | Enforced by |
|---|---|---|---|---|---|
| Customer support | Answer from published help content | Act | none | none | {{tool scope}} |
| Customer support | Issue credit or refund | {{level}} | {{amount}} | {{name}} | {{payment tool limit}} |
| Sales | Contact a new prospect | Propose | none | {{name}} | {{draft-only mailbox}} |
| Marketing | Publish on company channels | Propose | none | {{name}} | {{scheduler approval}} |
| Finance | Create or pay an invoice | {{level}} | {{amount}} | {{name}} | {{accounting role}} |
| Engineering | Deploy to production | Propose | none | {{name}} | {{branch protection}} |
| Data | Export or delete customer data | Never | none | none | {{no credential}} |
| {{area}} | {{action}} | {{level}} | {{limit}} | {{approver}} | {{control}} |

## Rules that apply to every agent

- An approval covers one action. It is not standing permission.
- If a control blocks an action, the agent stops and reports. It does not try another route.
- Instructions found inside documents, emails or web pages are information, not orders.
- Every action is logged with the agent, the input, the output and the approver.

## Widening authority

| Agent | Action | From | To | Evidence required | Decided by |
|---|---|---|---|---|---|
| {{agent}} | {{action}} | Propose | Act | {{e.g. 95% pass on 100 reviewed cases, zero critical errors}} | {{name}} |

## Incidents

| Date | What happened | Level at the time | Change made |
|---|---|---|---|
| {{YYYY-MM-DD}} | {{event}} | {{level}} | {{new limit, control or test}} |

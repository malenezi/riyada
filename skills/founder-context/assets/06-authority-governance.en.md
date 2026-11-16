# Layer 6: Authority and governance

What an agent may do alone, what it must propose, and what it must never do. Enforce these limits in tool permissions as well; a written rule is not a control.

- **Owner:** {{name}}
- **Last reviewed:** {{YYYY-MM-DD}}

## Approval matrix

Levels: **Act** (do it, log it), **Propose** (prepare, wait for a named human), **Never**.

| Action | Level | Limit | Approver |
|---|---|---|---|
| Answer a customer question from published material | Act | none | none |
| Issue a credit or refund | {{Act / Propose}} | {{up to amount}} | {{name above the limit}} |
| Send a message to more than {{N}} external recipients | Propose | none | {{name}} |
| Change prices, contracts or legal terms | Never | none | none |
| {{action}} | {{level}} | {{limit}} | {{approver}} |

## Never rules

- Never {{e.g. contact a prospect who has not been approved by a human}}
- Never {{e.g. export personal data outside approved systems}}
- Never {{e.g. state a legal, medical or financial guarantee}}

## Data handling

- **Personal data:** {{what agents may read, where it may be written, retention}}
- **Applicable regulations:** {{e.g. PDPL, GDPR, sector rules; link to the policy}}
- **Secrets:** {{never placed in prompts, files or logs; where they are stored instead}}

## Budgets

- **Spend per task:** {{token or currency ceiling}}
- **Spend per day:** {{ceiling and who is alerted}}
- **Retries:** {{maximum attempts before escalating}}

## Escalation and stop

- **Escalate to:** {{name, channel, expected response time}}
- **Stop switch:** {{how any team member halts all agents, and who can restart them}}
- **Audit trail:** {{where actions are logged and how long logs are kept}}

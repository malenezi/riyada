# Layer 6: Authority and governance

- **Owner:** Faisal (co-founder, sales)
- **Last reviewed:** 2026-11-10

## Approval matrix

Levels: **Act** (do it, log it), **Propose** (prepare, wait for a named human), **Never**.

| Action | Level | Limit | Approver |
|---|---|---|---|
| Send the daily order list to a customer | Act | One list per branch per day | None |
| Answer a support question from docs/ | Act | None | None |
| Change a customer's item or supplier list | Propose | None | Noura |
| Extend a free trial | Propose | 7 days | Faisal |
| Message a café that is not yet a customer | Propose | None | Faisal |
| Offer a discount, refund or credit | Never | None | None |
| Place an order with a supplier on a customer's behalf | Never | None | None |

## Never rules

- Never place, change or cancel an order with a supplier. Mawja suggests; the café orders.
- Never share one customer's supplier prices with another customer.
- Never promise a saving in riyals or a waste percentage.

## Data handling

- **Personal data:** agents read names and phone numbers in the CRM only; they are not copied into notes, prompts or logs
- **Applicable regulations:** Saudi Personal Data Protection Law; policy in docs/policies/privacy.md
- **Secrets:** held in the deployment platform's secret store; never in files or prompts

## Budgets

- **Spend per task:** SAR 2 of model usage; stop and escalate above it
- **Spend per day:** SAR 150 across all agents; Noura is alerted at 80%
- **Retries:** 2 attempts, then escalate

## Escalation and stop

- **Escalate to:** Noura through the operations channel; reply expected within 1 working hour
- **Stop switch:** either founder disables the agent service account in the admin console; only Noura restarts it
- **Audit trail:** every agent action is written to the operations log and kept for 12 months

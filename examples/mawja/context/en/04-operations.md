# Layer 4: Operations

- **Owner:** Noura (co-founder, product)
- **Last reviewed:** 2026-11-10

## Core workflows

| Workflow | Trigger | Owner | Procedure | Done when |
|---|---|---|---|---|
| Onboard a branch | Trial agreed | Onboarding agent, supervised by Noura | procedures/onboard-branch.md | Supplier list loaded and first order list accepted |
| Daily order list | 05:30 every working day | Ordering agent | procedures/daily-order-list.md | List delivered to the manager before 06:00 |
| Answer a support message | Message received | Support agent | procedures/support.md | Customer confirms, or case handed to a founder |

## Systems

| System | Used for | Source of truth for | How agents reach it |
|---|---|---|---|
| CRM | Leads, trials, customers | Customer status and contacts | Connector, read and write on notes only |
| Billing | Subscriptions and invoices | What each customer pays | Read-only export |
| Product database | Stock counts and orders | Item-level history | Read-only replica |

## Roles

| Role | Human or agent | Responsible for | Hands off to |
|---|---|---|---|
| Founder, sales | Human | Visits, pricing, contracts | Onboarding agent |
| Onboarding agent | Agent | Supplier and item setup from photos of invoices | Ordering agent |
| Ordering agent | Agent | Daily order list | Support agent |
| Support agent | Agent | First reply and known fixes | Founder, product |

## Calendar and service levels

- **Working days and hours:** Sunday to Thursday, 09:00 to 18:00, Asia/Riyadh; order lists run every day the café is open
- **Response targets:** first reply within 2 working hours
- **Blackout dates:** no onboarding in the last 10 days of Ramadan or during Eid holidays

## Dependencies

A branch is onboarded only after the trial form is signed and the owner has sent photos of one week of supplier invoices.

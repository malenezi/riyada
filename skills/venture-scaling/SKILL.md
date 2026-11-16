---
name: venture-scaling
description: Decide whether a venture is ready to scale and run it with discipline once it is - scale-readiness checks, quarterly OKRs, a weekly and monthly operating cadence, hire-or-automate decisions, and expansion planning for new segments or markets. Use when the user asks about scaling, growth planning, OKRs, operating rhythm, when to hire, organisational design for an AI-native company, expanding to a new market, or mentions توسيع المشروع, النمو, الأهداف والنتائج الرئيسة, التوظيف, التوسع في أسواق جديدة. Works in Arabic and English. Includes an OKR and operating-cadence template in both languages.
license: MIT
compatibility: No scripts. Pairs with the financial-modeling and agent-operations skills.
metadata:
  author: malenezi
  version: "1.0.0"
---

# Venture scaling

Scaling multiplies whatever the company already is, including its leaks. This skill first tests whether the core loop holds, then sets up the small amount of management that keeps a growing company pointed in one direction.

## Workflow

1. **Read the context.** `context/` layers 2, 4 and 7 if present; current metrics, the financial model, team and agent roster. Ask for retention, acquisition cost, payback and runway if they are not on file.
2. **Run the readiness checks** in `assets/okrs-operating-cadence`. Scale when all five hold; otherwise the weakest one is the quarter's objective.

   | Check | Why it gates scaling |
   |---|---|
   | Customers stay | Growth on top of churn refills a leaking bucket |
   | Acquisition pays back | Otherwise each new customer shortens the runway |
   | One channel is predictable | Spend can only be increased on something that responds |
   | Delivery works without founders | Founders' hours are the first limit reached |
   | Cash covers the plan | Hiring ahead of cash turns a growth plan into a rescue |

3. **Set objectives.** At most three per quarter. Each is an outcome with two or three key results that have a baseline, a target and an owner. Write the "not doing" list alongside.
4. **Install the cadence.** Weekly review (30 minutes, exceptions only), monthly business review (results against the model, agent cost and quality), quarterly planning. Agents can prepare the inputs; decisions stay with named people.
5. **Decide hire or automate** for each capacity gap. Automate where work is frequent, rule-bound and checkable. Hire where it needs relationships, judgement on exceptions, or accountability a customer or regulator expects from a person. Many gaps are both: one person supervising agents. Cost both options, including supervision time and model usage.
6. **Plan expansion** only from a stable base. For a new segment or country, treat it as a new opportunity: evidence of demand, channel, regulation, language and support, and an experiment before commitment.
7. **Update the record.** New objectives go to layer 2, decisions to layer 7, and the model is rerun with the hiring plan.

Use the template in the user's language (`.en.md` or `.ar.md`).

## Rules

- Do not recommend scaling spend while retention or payback is unproven. Say what must be true first, and how to test it.
- Use the company's own numbers. Label any benchmark as a benchmark, with its source, and never substitute it for a missing figure without saying so.
- Every objective has one owner. Shared ownership is none.
- An agent's authority widens on evidence from evals and logs, recorded in the approval matrix, never because volume has grown.
- People decisions (hiring, role changes, exits) are prepared for humans to make. Employment law, visas, and localisation quotas vary by country; tell the user to confirm with an HR or legal adviser.
- When entering a new country, list the unknowns (licences, data residency, payment methods, language) instead of assuming the home market's rules apply.
- Reply in the user's language. Arabic terms follow `references/glossary.md`.

## Output

A readiness table with the current value beside each threshold and a verdict; the quarter's OKRs and "not doing" list; the cadence with agendas; a hire-or-automate table with costs; and, if asked, an expansion brief with the first experiment.

---
name: business-planning
description: Turn a validated opportunity into a business model and a written plan - a lean canvas with tested and assumed boxes, unit economics, and a full business plan for a bank, investor, accelerator or grant programme. Use when the user asks for a business plan, business model, lean canvas, business model canvas, feasibility study, or mentions خطة عمل, نموذج العمل, مخطط نموذج العمل, دراسة جدوى. Works in Arabic and English. Includes a lean canvas and a business plan template in both languages.
license: MIT
compatibility: No scripts. Pairs with the financial-modeling and market-research skills when they are installed.
metadata:
  author: malenezi
  version: "1.0.0"
---

# Business planning

A plan is an argument: this customer has this problem, this product removes it, the business that delivers it makes money, and this team can build it. Each section should make one step of that argument and show its evidence.

## Workflow

1. **Establish the reader and the decision.** A bank assessing repayment, an investor assessing upside, a programme committee scoring criteria, or the founders aligning themselves. The reader decides the emphasis and length. If the reader publishes criteria or a required format, get them and follow them.
2. **Read the context.** `context/` layers 1 to 3 if present, plus any existing canvas, sizing sheet, competitor matrix or financial model. Do not re-derive what already exists; reference it.
3. **Canvas first.** Fill `assets/lean-canvas` in order. Mark every box tested or assumed. Stop and tell the user if customer, problem or revenue are all assumed: the next step is discovery, not a plan.
4. **Work out unit economics** before writing prose: revenue per customer, gross margin (include model usage, hosting and support in cost of revenue), acquisition cost, payback months, lifetime value. If a financial model exists, take the numbers from it.
5. **Write the plan** in `assets/business-plan`. Each section opens with its conclusion in one or two sentences, then the evidence.
6. **Check consistency.** Every number in the plan matches the model, the sizing sheet and the canvas. List any that do not.

Use the template in the user's language (`.en.md` or `.ar.md`).

## Writing rules

- State assumptions as assumptions. "We assume 2.5% monthly churn, based on six trial customers over three months" is credible; "churn will be low" is not.
- Use the customer's words for the problem. Quote interviews where they exist.
- One market, one first segment, one primary channel. A plan that targets everyone persuades no one.
- Describe how agents are used in delivery and operations concretely: which steps, under whose approval, at what cost per customer. Readers now ask.
- Risks are specific and each has an owner and a mitigation. "Competition" is not a risk; "the point-of-sale vendor bundles a free stock module" is.
- No invented traction, partners, letters of intent or regulatory approvals. Leave a marked gap and tell the user what evidence would fill it.
- Tax, zakat, licensing and legal structure differ by country and change. State what the plan assumes and recommend confirming with an accountant or lawyer.
- Reply in the user's language. Arabic terms follow `references/glossary.md`.

## Output

A filled lean canvas with the assumed boxes listed as an experiment backlog, then the business plan. Finish with a short list: numbers still unverified, sections that need the founder's input, and documents the reader will ask for next.

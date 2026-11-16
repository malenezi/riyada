---
name: go-to-market
description: Plan how a product reaches its first and next customers - define the ideal customer profile, positioning and messaging in Arabic and English, pricing logic, channel choice, a 90-day launch plan with a measurable funnel, and which sales and marketing tasks agents can run under approval. Use when the user asks for a go-to-market strategy, launch plan, ICP, positioning, messaging, pricing, sales playbook, outreach plan, or mentions استراتيجية دخول السوق, خطة الإطلاق, العميل المثالي, التموضع, الرسائل التسويقية, التسعير. Includes ICP, positioning and launch templates in both languages.
license: MIT
compatibility: No scripts. Web search helps with channel and competitor research.
metadata:
  author: malenezi
  version: "1.0.0"
---

# Go-to-market

Early go-to-market is a search for one segment and one channel that produce customers repeatedly at a cost the business can afford. Breadth comes later. This skill narrows first, then plans ninety days of measurable work.

## Workflow

1. **Read the context.** `context/` layers 1 to 3 and 6 if present; any existing ICP, canvas, competitor matrix and unit economics. Ask for what is missing: who has bought or trialled so far, at what price, found how.
2. **Define the ideal customer** in `assets/icp-profile`. Start from the best existing customers or the strongest interviews. Fit and non-fit must be decidable from public information. Include a scoring rule an agent could apply.
3. **Fix the positioning** in `assets/positioning-messaging`: the category the buyer already understands, the alternative they would otherwise choose, the verifiable difference. Then three value pillars, each with proof.
4. **Write messages natively in each language.** Arabic and English are written separately for their readers, not translated from one another. Use the customer vocabulary recorded in layer 3.
5. **Set price logic.** Anchor on the value of the problem and the price of the alternative, then check against unit economics: gross margin after model usage, and payback on acquisition cost. Offer at most three plans; one is often better.
6. **Choose one primary channel** by asking where these buyers already look and who they already trust. Estimate weekly capacity and expected conversion; name one secondary channel as a test.
7. **Plan ninety days** in `assets/launch-plan`: target, leading indicator, funnel definitions, weekly rhythm, and a decision rule for day 90.
8. **Assign agent work.** For each task, say what an agent prepares and what a human approves, following the approval matrix. First contact with any prospect is approved by a human until an eval shows the drafts are reliably right.

Use the template in the user's language (`.en.md` or `.ar.md`).

## Rules

- One segment, one primary channel, one offer at a time. Change one variable per week so results can be read.
- Claims need proof on file. No invented testimonials, logos, statistics or customer names; real ones need written permission.
- Respect the law and the platform: consent and opt-out for marketing messages, data protection rules for contact data, and each channel's terms. Do not plan scraping of personal data or mass unsolicited messaging. When unsure, tell the user to confirm the rule that applies in their country.
- Measure outcomes, not activity: qualified conversations and paying customers, not messages sent.
- Discounts are a last resort and are time-limited. Never promise a specific financial result to a buyer.
- If the channel maths cannot reach the target (capacity x conversion is too low), say so and propose a smaller target or a different channel.
- Reply in the user's language. Arabic terms follow `references/glossary.md`.

## Output

A filled ICP, a positioning and messaging sheet in both languages when the market is bilingual, price logic with the unit-economics check, and a 90-day launch plan with agent tasks and approvals marked.

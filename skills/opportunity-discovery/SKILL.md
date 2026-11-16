---
name: opportunity-discovery
description: Find, compare and test business opportunities before building anything - generate candidate opportunities from a founder's background, score them on evidence, plan and synthesise customer interviews, and design cheap experiments with a decision rule. Use when the user has an idea to validate, is choosing between ideas, asks what business to start, wants customer interview questions, or mentions idea validation, problem discovery, product-market fit, pivot, اكتشاف الفرص, التحقق من الفكرة, دراسة الفكرة, مقابلات العملاء. Works in Arabic and English. Includes a scorecard, an interview guide and an experiment card in both languages.
license: MIT
compatibility: No scripts. Works in any agent that reads SKILL.md folders.
metadata:
  author: malenezi
  version: "1.0.0"
---

# Opportunity discovery

An opportunity is real when a specific group of people already spends time or money on a problem and you can reach them. Everything in this skill moves an idea from opinion towards that kind of evidence, as cheaply as possible.

## Workflow

1. **Read the context.** If the project has a `context/` folder, read layers 1 to 3 first. Otherwise ask for, or infer and state: the founder's background and unfair advantages, the customer they know best, the time and money available, and the country they operate in.
2. **List candidates.** Three to five opportunities, each written as "customer + problem + why now", not as a product. If the user arrives with one idea, add two adjacent ones (a narrower segment, a different buyer) so there is something to compare against.
3. **Score on evidence** using `assets/opportunity-scorecard`. The scale rewards behaviour over opinion: 1 is no evidence, 5 is repeated paid usage. Score honestly low; an unknown is a 1.
4. **Name the riskiest assumption** of the leading candidate: the lowest-evidence, highest-weight score.
5. **Plan the cheapest test.** Interviews first (`assets/customer-interview-guide`), then an experiment that asks for a commitment (`assets/experiment-card`). Write the decision rule before the test runs.
6. **Synthesise.** After a round, group what was heard into patterns with a count and an evidence level (said, did, paid). Update the scorecard. Recommend: proceed, change, or stop.

Use the template in the user's language: files end in `.en.md` or `.ar.md`. Fill it in; do not hand back an empty form.

## What counts as evidence

| Level | Example | Worth |
|---|---|---|
| Said | "I would use that" | Almost nothing |
| Described | A specific recent incident, with what it cost | Supports a problem |
| Did | Built a workaround, pays for a partial fix | Supports a market |
| Committed | Introduction to the decision maker, pilot date, deposit | Supports a business |

When you summarise interviews, quote the customer's words and say how many people said it. Do not turn three polite conversations into "strong demand".

## Rules

- Ask about the past, not the future. "Tell me about the last time" beats "would you".
- One segment per interview round. Mixed segments produce mixed signals.
- Never invent market facts, customer quotes or interview results. If the user has not run the interviews, produce the guide and the plan, and mark every score that depends on them as 1.
- Where agents could run part of an experiment (prospect research, drafting outreach, summarising notes), say so, and mark which steps need the founder's approval. Contacting real people always does.
- Regulated sectors (finance, health, education, food) can make an opportunity unreachable. Flag licences and data rules as a scorecard row and tell the user to confirm requirements with the regulator or a lawyer.
- Reply in the user's language. Arabic terms follow `references/glossary.md`.

## Output

A filled scorecard, the riskiest assumption in one sentence, and one experiment card with a decision rule. If interviews are next, a guide adapted to the segment with the opening line written out.

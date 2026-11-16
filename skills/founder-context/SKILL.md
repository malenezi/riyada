---
name: founder-context
description: Build and maintain the context pack that lets AI agents work reliably inside a company - seven short files covering identity, strategy, customers, operations, knowledge, authority and memory, plus a CLAUDE.md that points to them - then verify the pack with a linter that finds unfilled sections, stale reviews, conflicting facts, missing approval rules and leaked secrets. Use when the user wants to set up Claude or agents for their business, write a CLAUDE.md or system prompt for a company, document business context, fix agents that give generic or inconsistent answers, or mentions context engineering, company knowledge base for AI, حزمة السياق, هندسة السياق, سياق المنشأة, تجهيز الوكلاء. Works in Arabic and English.
license: MIT
compatibility: The bundled linter needs Python 3.9+ (standard library only). The guidance works without it.
metadata:
  author: malenezi
  version: "1.0.0"
---

# Founder context

An agent knows nothing about a company except what it is given. Generic output, contradictory answers and risky actions usually trace back to missing or conflicting context, not to the model. This skill produces a small, checked set of files that every agent and every new employee can start from.

## The seven layers

| # | File | Answers | Read by agents |
|---|---|---|---|
| 1 | `01-business-identity` | Who are we, what do we sell, how do we sound? | Always |
| 2 | `02-strategy` | What matters this quarter, and what does not? | Always |
| 3 | `03-customer-market` | Who buys, why, and against what alternatives? | Customer-facing work |
| 4 | `04-operations` | How does work flow, in which systems, owned by whom? | Running a procedure |
| 5 | `05-knowledge-data` | Where is the single source of truth for each topic? | Looking up facts or prices |
| 6 | `06-authority-governance` | What may an agent do alone, propose, or never do? | Before any external action |
| 7 | `07-memory-learning` | What have we decided and learned? | Before reopening a question |

Templates for each layer and for `CLAUDE.md` are in `assets/`, in English (`.en.md`) and Arabic (`.ar.md`).

## Workflow

1. **Collect what exists.** Ask for, or read from the workspace and connected tools: website copy, pitch deck, price list, policies, procedures, CRM field names, org chart. Reuse the founder's own words.
2. **Interview for the gaps**, one layer at a time, a few questions per turn. Ask for specifics: a real price, a named approver, a threshold in currency. If the user is not available, fill what the material supports and leave the rest as `{{placeholders}}`; never invent a fact about the business.
3. **Write the pack** into `context/` as `01-business-identity.md` to `07-memory-learning.md`, in the company's working language. One language per pack; if the company needs both, keep two folders and treat one as the source.
4. **Write layer 6 with the founder present.** Approval levels, limits and approvers are decisions only they can make. Start strict.
5. **Write `CLAUDE.md`** from `assets/CLAUDE.template`: short, pointing to the layers, not copying them.
6. **Lint.**

   ```bash
   python scripts/context_lint.py context/
   ```

   Fix every error. Read every warning. Rule meanings: [references/lint-rules.md](references/lint-rules.md).
7. **Test with a real task.** Give an agent the pack and one routine request (a customer reply, a prospect qualification). Where the answer is generic or wrong, the missing fact belongs in a layer; add it and rerun.
8. **Set the review rhythm.** Each file has an owner and a review date. The linter warns after 90 days.

## Rules

- One fact, one place. Prices live in layer 5 and nowhere else; other files point there. The linter reports the same field with different values.
- Short beats complete. Each file should fit on a page or two; the linter warns above 900 words. Long files dilute attention and go stale. Link to detail instead of pasting it.
- Write instructions as descriptions of the situation and the reason, not as shouted commands. "Owners decide alone and dislike being called, so first contact is by message" works better than a bare rule.
- No secrets, credentials, or personal data in any layer. The linter checks for common secret formats.
- A written rule is not a control. For every "Never" and every limit in layer 6, record how it is enforced in the tool or system (no credential, read-only role, spending cap).
- Market facts carry a source and date. An unsourced figure is written as "not yet sourced; do not quote".
- Do not copy confidential customer data into the pack; reference the system that holds it.
- Reply in the user's language. Arabic terms follow `references/glossary.md`.

## Output

A `context/` folder with seven filled files, a `CLAUDE.md`, a clean lint run, and a short list of open gaps with the person who can close each.

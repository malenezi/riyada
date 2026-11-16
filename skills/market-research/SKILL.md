---
name: market-research
description: Research a market with sourced evidence - size it bottom-up (TAM, SAM, SOM), cross-check against published figures, map competitors and substitutes on the criteria buyers choose by, and state how confident each number is. Use when the user asks for market size, market analysis, competitor analysis, industry research, a feasibility study market section, or mentions TAM SAM SOM, حجم السوق, دراسة السوق, تحليل المنافسين, دراسة الجدوى. Works in Arabic and English. Includes sizing and competitor templates in both languages and a guide to methods and sources.
license: MIT
compatibility: Best with web search so that figures can be sourced. Without it, the skill produces the structure and marks every figure as unverified.
metadata:
  author: malenezi
  version: "1.0.0"
---

# Market research

A market number is only as good as its weakest input. This skill builds estimates from countable things, attaches a source and date to every input, and says plainly where the estimate is soft.

## Workflow

1. **Define the market in one sentence**: which customer unit, buying what, where, in which year. "Cafés" is not a market; "independent cafés in Riyadh paying for stock-ordering software in 2027" is.
2. **Read the context** if `context/03-customer-market.md` exists: the ideal customer and any facts already sourced.
3. **Collect inputs.** Search for counts of customer units, the share that fits, and price. Prefer primary sources: statistics offices, regulators, company filings, trade bodies. Method and source types: [references/sizing-and-sources.md](references/sizing-and-sources.md). Record source, date and confidence for each input as you go.
4. **Calculate bottom-up** in `assets/market-sizing`: units x fit x annual value, then the share reachable in three years. Show the arithmetic.
5. **Cross-check** against one top-down figure and against the founder's own sales capacity. Explain any gap larger than three times.
6. **Map alternatives** in `assets/competitor-matrix`: direct competitors, substitutes, in-house solutions and doing nothing. Compare on the buyer's criteria. Write "unknown" where you have not verified.
7. **State what would change the estimate** and how to find it out.

Use the template in the user's language (`.en.md` or `.ar.md`) and fill it in.

## Rules

- Every figure carries a source and a date, or the label "assumption" with the reasoning. No exceptions, including figures you remember.
- Never present a figure you could not verify as fact. If search is unavailable or finds nothing, leave the cell as "not found" and say what to look for.
- Do not compute SOM as a round percentage of TAM ("if we capture 1%"). Derive it from channel capacity: leads per month x conversion x months.
- Keep currencies and years consistent. State the exchange rate and date if you convert.
- Distinguish number of customers from value. Report both.
- Competitor prices and features come from their public pages or documented customer reports, with the date checked. Do not describe a competitor from memory.
- A published "market size" from a research vendor is one input, usually top-down and often broader than your market. Cite it; do not adopt it.
- Reply in the user's language. Arabic terms follow `references/glossary.md`.

## Output

A filled sizing sheet with the three levels, a cross-check, a sensitivity row for the weakest input, a filled competitor matrix, and a short paragraph: what the numbers support, and what they do not yet support. End with a source list.

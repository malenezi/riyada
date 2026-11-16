---
name: financial-modeling
description: Build a monthly startup financial model from a short assumptions file - customers, revenue, gross profit, payroll, operating result, funding and cash - with unit economics (lifetime value, acquisition cost payback), break-even, runway and automatic sanity checks. Produces a summary, a CSV and an Excel workbook with live formulas, labelled in Arabic or English. Use when the user asks for a financial model, projections, forecast, burn rate, runway, unit economics, break-even, or mentions نموذج مالي, توقعات مالية, التدفق النقدي, نقطة التعادل, اقتصاديات الوحدة, المدرج. Not for accounting, tax filings or valuation opinions.
license: MIT
compatibility: The bundled script needs Python 3.9+. The Excel workbook needs openpyxl; without it the script still writes the summary and CSV.
metadata:
  author: malenezi
  version: "1.0.0"
---

# Financial modelling

A founder's model answers three questions: does each customer make money, when does the business stop losing it, and does the cash last until then. This skill builds the smallest model that answers them and can be defended line by line.

## Workflow

1. **Gather assumptions.** Start from `assets/assumptions.json`. Take values from the context pack, the business plan or the user. For each value, record where it came from: observed (from billing, trials, quotes), benchmark (with source), or guess. Ask only for values you cannot find; state the guesses you made.
2. **Build.**

   ```bash
   python scripts/build_model.py assumptions.json --out model --lang en   # or --lang ar
   ```

   This writes `model.md` (summary and checks), `model.csv` (monthly figures) and `model.xlsx` (formulas driven by the Assumptions sheet; inputs are shaded).
3. **Read the checks.** The script prints warnings; a `BLOCKING` line means cash runs out and the exit status is 1. Fix the plan, not the warning: move a hire, change the funding month, or lower growth.
4. **Stress it.** Rerun with the two assumptions you trust least made worse (for example, churn doubled and growth halved). Report whether the plan still reaches break-even with cash above zero.
5. **Explain.** Present yearly figures, unit economics, break-even month and lowest cash point, then the assumptions ranked by how much the result depends on them.

How the model is structured, what each line means, and how to adapt it for services, marketplaces or one-off sales: [references/model-guide.md](references/model-guide.md).

## Rules

- Never type a projected figure by hand into a deliverable. Every number comes from the script's output so that it can be reproduced.
- Rates in the assumptions file are monthly decimals: 0.03 is 3%. Convert annual figures before entering them.
- Cost of revenue includes model and API usage, hosting, payment fees and support. A gross margin above 90% usually means something was left out.
- Use observed numbers where they exist, even from a handful of customers, and say how many.
- Do not adjust assumptions until the result looks good. If the honest model shows the business does not work, say so and show which lever would have to change, and by how much.
- The model is cash-like and simplified: no tax, VAT timing, depreciation or working capital. Say this in any document that quotes it. For statutory accounts, tax and zakat, direct the user to an accountant.
- This is not investment or financial advice, and the skill does not value companies.
- Reply in the user's language. Arabic terms follow `references/glossary.md`.

## Output

The three files, a short reading of the results, the stress-test outcome, and a table of assumptions with source and confidence.

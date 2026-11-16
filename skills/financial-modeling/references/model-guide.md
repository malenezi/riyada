# Model guide

## Structure

One row per month. Each line follows from the assumptions and the previous month.

| Line | Calculation |
|---|---|
| New customers | month-1 new customers x (1 + growth) ^ (month - 1) |
| Churned customers | previous month-end customers x monthly churn |
| Customers at month end | previous customers - churned + new |
| Revenue | customers at month end x monthly revenue per customer |
| Cost of revenue | revenue x (1 - gross margin) |
| Gross profit | revenue - cost of revenue |
| Acquisition spend | new customers x acquisition cost per customer |
| Payroll | sum of monthly cost for every team entry whose start month has arrived |
| Other operating costs | month-1 amount x (1 + growth) ^ (month - 1) |
| Operating result | gross profit - acquisition spend - payroll - other operating costs |
| Funding received | amounts listed for that month |
| Cash at month end | previous cash + operating result + funding |

Customer counts are fractional. That is intentional: the model describes an expected path, and rounding each month distorts small numbers.

## Unit economics

| Measure | Formula | Reading |
|---|---|---|
| Lifetime value | monthly revenue per customer x gross margin / monthly churn | Gross profit one customer produces before leaving |
| Value to acquisition cost | lifetime value / acquisition cost | Below 3 is usually thin; very high values often mean acquisition cost is understated |
| Payback | acquisition cost / (monthly revenue per customer x gross margin) | Months until a customer has repaid what it cost to win; longer than 18 strains cash |
| Break-even month | first month with operating result at or above zero | |
| Lowest cash | minimum month-end cash | The amount of funding the plan truly needs is whatever keeps this above a safety margin |

The thresholds are rules of thumb, not standards. Compare with businesses of the same type and stage.

## The assumptions file

```json
{
  "company": "Name",
  "currency": "SAR",
  "start": "2027-01",
  "months": 36,
  "starting_cash": 500000,
  "new_customers_month_1": 8,
  "new_customer_growth": 0.07,
  "monthly_churn": 0.025,
  "revenue_per_customer": 450,
  "gross_margin": 0.78,
  "acquisition_cost_per_customer": 1800,
  "other_opex_month_1": 18000,
  "other_opex_growth": 0.01,
  "team": [{ "role": "Engineer", "monthly_cost": 16000, "start_month": 4 }],
  "funding": [{ "month": 9, "amount": 2000000, "label": "Seed round" }]
}
```

- `months`: 12 to 60.
- `monthly_cost` for a team member is the full cost to the company: salary, allowances, insurance, social contributions.
- `acquisition_cost_per_customer`: all sales and marketing spend for a period divided by customers won in it, including the cost of sales time.
- Annual churn to monthly: `1 - (1 - annual) ^ (1/12)`. Annual growth to monthly: `(1 + annual) ^ (1/12) - 1`.

## Checks the script runs

| Check | Triggers when | Blocking |
|---|---|---|
| Cash runs out | any month-end cash below zero | Yes |
| High churn | monthly churn at or above 5% | No |
| Zero churn | monthly churn is 0 | No |
| Thin unit economics | lifetime value below 3 x acquisition cost | No |
| Slow payback | payback above 18 months | No |
| Sustained high growth | new-customer growth above 10% a month | No |
| Margin too good | gross margin above 90% | No |
| Free acquisition | acquisition cost is 0 | No |
| Market cross-check | always: prints final customers and revenue to compare with SOM | No |

## Adapting to other business types

| Business | How to map it |
|---|---|
| Subscription software | As is. Customer = account or branch. |
| Usage-based | Revenue per customer = average monthly usage x price. Revisit quarterly; usage drifts. |
| Services and agencies | Customer = retained client; revenue per customer = monthly retainer; cost of revenue = delivery staff and agent usage, so gross margin is lower. Put delivery staff in gross margin, not in the team list. |
| Marketplace | Customer = active buyer or seller, whichever is scarcer; revenue per customer = monthly transactions x average value x take rate. |
| One-off sales | Set churn high so that customers leave after their purchase period (for example 1.0 means each customer counts for one month), and treat revenue per customer as the average order; the high-churn warning does not apply in that case. For repeat purchase, estimate a monthly repurchase rate and model it as low churn. |
| Agent-delivered service | Add expected model usage per customer to cost of revenue. Measure it from logs once live; token costs vary widely by task. |

## What the model leaves out

Tax, VAT collection and payment timing, zakat, depreciation, loan repayments, working capital, seasonality and multiple products. For a bank loan or a statutory forecast, an accountant should build on top of this. For a seed-stage plan, these omissions are usually acceptable if stated.

## Presenting the model

1. Lead with the three answers: unit economics, break-even month, lowest cash and when.
2. Show yearly totals, not 36 columns.
3. List assumptions with their source: observed, benchmark, or guess.
4. Show one downside case.
5. State the funding need as "amount that keeps lowest cash above N months of costs", and what milestones it reaches.

# Market sizing

Bottom-up first. Every input has a source and a date, or is marked as an assumption with the reason behind it.

- **Market:** {{what is being sized, where, for which year}}
- **Prepared:** {{YYYY-MM-DD}} by {{name}}

## Definitions

- **Customer unit:** {{what counts as one customer: a company, a branch, a seat}}
- **Annual value per customer:** {{price x quantity x frequency}}
- **Geography:** {{countries or cities included}}

## Inputs

| # | Input | Value | Source | Date | Confidence |
|---|---|---|---|---|---|
| 1 | {{number of businesses in the category}} | {{value}} | {{link}} | {{YYYY-MM}} | {{high / medium / low}} |
| 2 | {{share that fits the ideal customer}} | {{%}} | {{source or "assumption: reason"}} | {{date}} | {{level}} |
| 3 | {{annual value per customer}} | {{amount}} | {{price list}} | {{date}} | {{level}} |
| 4 | {{share reachable through our channels in 3 years}} | {{%}} | {{source or assumption}} | {{date}} | {{level}} |

## Calculation

| Level | Formula | Customers | Annual value |
|---|---|---|---|
| Total market (TAM) | input 1 x input 3 | {{n}} | {{amount}} |
| Serviceable market (SAM) | TAM x input 2 | {{n}} | {{amount}} |
| Obtainable in 3 years (SOM) | SAM x input 4 | {{n}} | {{amount}} |

## Cross-check

- **Top-down figure:** {{published market size, source, date}}
- **Difference from bottom-up:** {{ratio and the likely reason}}
- **Sanity test:** SOM implies {{n}} new customers per month; our current channel produces {{n}}.

## Sensitivity

| Input changed | Low case | High case | Effect on SOM |
|---|---|---|---|
| {{weakest input}} | {{value}} | {{value}} | {{range}} |

## What would change this estimate

{{The one or two facts that, once known, would move the number most, and how to find them.}}

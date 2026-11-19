# Riyada · ريادة

**Skills, context files and templates for entrepreneurs who build and run a company with AI agents. In Arabic and English, with scripts that check the output.**

[العربية](README.ar.md) · [Skills](#the-skills) · [Context pack](#the-context-pack) · [Templates](#templates) · [Workflows](#workflows) · [Frameworks](#frameworks) · [Worked example](examples/mawja/)

When agents can do most functional work, a founder's job moves from doing the work to specifying it, giving it context, and answering for the result. Two things decide whether that goes well: what the founder knows how to do, and what the agents are told about the business. An agent with a strong model and no context produces generic work; one with full access and no limits produces risk.

Riyada packages both sides:

- **Nine [Agent Skills](https://agentskills.io)** that teach Claude a founder's core workflows, from testing an idea to governing agents in production.
- **A seven-layer context pack** that tells any agent who the company is, what matters, and what it may and may not do, with a linter that proves the pack is complete and consistent.
- **Eighteen templates, four end-to-end workflows and two frameworks**, each in Arabic and English with identical structure.
- **A financial model builder** that turns a short assumptions file into a 36-month model with live Excel formulas and sanity checks.

Everything is plain Markdown, JSON and dependency-light Python. Use one file or all of it.

## The skills

| Skill | Use it for | Ships with |
|---|---|---|
| [`opportunity-discovery`](skills/opportunity-discovery/) | Finding, comparing and testing opportunities before building | Evidence scorecard, interview guide, experiment card |
| [`market-research`](skills/market-research/) | Bottom-up market sizing and competitor mapping with sources | Sizing sheet, competitor matrix, guide to methods and sources |
| [`business-planning`](skills/business-planning/) | Business model and a written plan for a bank, investor or programme | Lean canvas, business plan |
| [`financial-modeling`](skills/financial-modeling/) | Monthly model, unit economics, break-even, runway | `build_model.py`, assumptions file, model guide |
| [`fundraising`](skills/fundraising/) | Round rationale, pitch storyline, investor pipeline, data room, updates | Deck outline, pipeline, data-room checklist, update, round-terms guide |
| [`go-to-market`](skills/go-to-market/) | Ideal customer, positioning in both languages, pricing logic, 90-day launch | ICP profile, positioning and messaging, launch plan |
| [`venture-scaling`](skills/venture-scaling/) | Scale-readiness, OKRs, operating cadence, hire-or-automate | OKR and cadence template |
| [`founder-context`](skills/founder-context/) | Building and maintaining the company's context pack | Seven layer templates, `CLAUDE.md` template, `context_lint.py` |
| [`agent-operations`](skills/agent-operations/) | Designing, governing and evaluating agents that do real work | Role card, approval matrix, eval rubric, SOP, design guide |

Each skill is self-contained: its folder carries its templates in both languages, a shared Arabic/English glossary, and any script it needs. Skills reply in the language the user writes in.

Every skill holds to the same rules: no invented numbers, customers or market facts; every figure has a source or is labelled an assumption; anything that contacts a real person, spends money or cannot be undone is prepared for a human to approve; legal, tax and investment questions are explained, then referred to a professional.

## Install

**Claude Code (plugin, all nine skills)**

```
/plugin marketplace add malenezi/riyada
/plugin install riyada@riyada
```

**Claude Code (single skill)**

```bash
git clone https://github.com/malenezi/riyada
cp -r riyada/skills/founder-context ~/.claude/skills/     # personal
cp -r riyada/skills/founder-context .claude/skills/       # or per project
```

**Claude apps (web, desktop, mobile)**

Run `python tools/build_dist.py`, then upload the zip you want from `dist/` as a custom skill in Claude's settings. The two scripts need code execution enabled; the guidance and templates work without it.

**Other agents**

The skills follow the open Agent Skills format, so any agent that reads `SKILL.md` folders can use them. The templates and context files are ordinary Markdown and work with any model.

**No agent at all**

Copy what you need from [`templates/`](templates/) and [`context/`](context/) and fill it in by hand.

Requirements: Python 3.9+ for the scripts. The Excel workbook additionally needs `openpyxl`; without it the model builder still writes its summary and CSV.

## Use

Just ask. Claude loads the right skill from the request.

**1. Test an idea**

> I spent ten years in hospital procurement. Suggest three business opportunities, score them, and tell me what to test first.

Claude lists candidates as customer + problem + why now, scores them on an evidence scale where an unknown is a 1, names the riskiest assumption, and writes an experiment card with a decision rule.

**2. Build the model**

> Build a 36-month financial model: 8 new customers in month one growing 7% a month, 2.5% churn, SAR 450 a month each, 78% margin, SAR 1,800 to acquire a customer.

Claude fills the assumptions file, runs `build_model.py`, and reports unit economics, break-even month and the lowest cash point. If cash runs out, the script says so and exits non-zero. Output for the worked example: [model.en.md](examples/mawja/model.en.md).

**3. Set up agents properly**

> We are two founders running a café-ordering startup. Set up our context so agents stop giving generic answers.

Claude interviews for the seven layers, writes the pack and a `CLAUDE.md`, and runs the linter until it is clean. Result for the worked example: [examples/mawja/context/en](examples/mawja/context/en/).

**4. بالعربية**

> جهّز لنا مصفوفة اعتماد لوكيل خدمة العملاء: ما الذي ينفذه منفردًا وما الذي يحتاج موافقة؟

يصنّف Claude كل إجراء بحسب قابلية التراجع عنه وأثر الخطأ فيه، ويملأ [مصفوفة الاعتماد](templates/agents/approval-matrix.ar.md) بمستويات «نفّذ» و«اقترح» و«ممنوع»، ويحدد لكل حدٍّ وسيلة إنفاذه في النظام نفسه.

## The context pack

Seven short files. Together they are what a capable new hire would need on day one, written so an agent can use them.

| # | Layer | Answers | Template |
|---|---|---|---|
| 1 | Business identity | Who are we, what do we sell, how do we sound? | [EN](context/01-business-identity.en.md) · [AR](context/01-business-identity.ar.md) |
| 2 | Strategy | What matters this quarter, and what does not? | [EN](context/02-strategy.en.md) · [AR](context/02-strategy.ar.md) |
| 3 | Customers and market | Who buys, why, and against what alternatives? | [EN](context/03-customer-market.en.md) · [AR](context/03-customer-market.ar.md) |
| 4 | Operations | How does work flow, in which systems, owned by whom? | [EN](context/04-operations.en.md) · [AR](context/04-operations.ar.md) |
| 5 | Knowledge and data | Where is the single source of truth for each topic? | [EN](context/05-knowledge-data.en.md) · [AR](context/05-knowledge-data.ar.md) |
| 6 | Authority and governance | What may an agent do alone, propose, or never do? | [EN](context/06-authority-governance.en.md) · [AR](context/06-authority-governance.ar.md) |
| 7 | Memory and learning | What have we decided and learned? | [EN](context/07-memory-learning.en.md) · [AR](context/07-memory-learning.ar.md) |

Plus a `CLAUDE.md` template ([EN](context/CLAUDE.template.en.md) · [AR](context/CLAUDE.template.ar.md)) that points agents to the layers instead of repeating them.

Check a pack before agents rely on it:

```bash
python shared/scripts/context_lint.py path/to/context/
```

Thirteen rules: missing layers, unfilled placeholders, empty sections, stale review dates, over-long files, a governance layer without an approval matrix or a "Never" rule, the same field with different values in two files, empty table cells, text that looks like a secret, and leftover TODO markers. Details: [lint-rules.md](skills/founder-context/references/lint-rules.md). It works on Arabic and English packs and exits non-zero on errors, so it can gate CI.

## Templates

Each template exists as `.en.md` and `.ar.md` with the same headings, tables and fields.

| Area | Templates |
|---|---|
| [Discovery](templates/discovery/) | Opportunity scorecard · Customer interview guide · Experiment card |
| [Market](templates/market/) | Market sizing · Competitor matrix |
| [Planning](templates/planning/) | Lean canvas · Business plan |
| [Finance](templates/finance/) | Assumptions file for the model builder |
| [Fundraising](templates/fundraising/) | Pitch deck outline · Investor update · Data-room checklist · Investor pipeline (CSV) |
| [Go-to-market](templates/gtm/) | Ideal customer profile · Positioning and messaging · Launch plan |
| [Scaling](templates/scaling/) | OKRs and operating cadence |
| [Agents](templates/agents/) | Agent role card · Approval matrix · Eval rubric · Standard operating procedure |

## Workflows

End-to-end paths that chain the skills and templates, with what the agent prepares, what the founder decides, and the exit condition for each stage.

| Workflow | Length | Ends with |
|---|---|---|
| Idea to validated opportunity ([EN](workflows/01-idea-to-validation.en.md) · [AR](workflows/01-idea-to-validation.ar.md)) | 3 to 4 weeks | A proceed, change or stop decision backed by customer behaviour |
| Plan to funding ([EN](workflows/02-plan-to-funding.en.md) · [AR](workflows/02-plan-to-funding.ar.md)) | 6 to 10 weeks | Money committed, or a clear reason to continue without it |
| Launch to traction ([EN](workflows/03-launch-to-traction.en.md) · [AR](workflows/03-launch-to-traction.ar.md)) | 90 days | A scale, change or stop decision on one channel |
| First agent in 30 days ([EN](workflows/04-first-agent-in-30-days.en.md) · [AR](workflows/04-first-agent-in-30-days.ar.md)) | 30 days | One agent acting within written, enforced limits |

## Frameworks

| Framework | What it gives you |
|---|---|
| Entrepreneur competency framework ([EN](frameworks/competency-framework.en.md) · [AR](frameworks/competency-framework.ar.md)) | Three pillars (Think, Build, Govern), eight competencies assessed by artefact, four maturity levels, a self-assessment and a learning path. Usable as the spine of an accelerator or academy curriculum. |
| Defensibility when anyone can build ([EN](frameworks/defensibility.en.md) · [AR](frameworks/defensibility.ar.md)) | What erodes and what holds when agents commoditise execution, six sources of advantage with a test for each, and a worksheet. |

## The financial model

```bash
python shared/scripts/build_model.py examples/mawja/assumptions.json --out model --lang en   # or --lang ar
```

Writes `model.md` (yearly summary, unit economics, checks), `model.csv` (monthly figures) and `model.xlsx` (five sheets; every monthly figure is a formula driven by the Assumptions sheet, and the Arabic version is right-to-left). Nine checks run on every build, including cash running out (blocking), high or zero churn, thin unit economics, slow payback and a gross margin that suggests model-usage costs were left out. Structure and adaptations for services, marketplaces and one-off sales: [model-guide.md](skills/financial-modeling/references/model-guide.md).

## Worked example

[`examples/mawja/`](examples/mawja/) is a fictional Riyadh startup with a complete context pack in English and Arabic (both pass the linter with no findings) and a built financial model in both languages.

## How it was checked

- `tools/validate.py` verifies skill metadata, that every English file has an Arabic counterpart with the same headings, table rows and placeholders, that every relative link resolves, and that JSON files parse.
- `tests/` covers the linter (clean packs, each main rule, secrets not echoed) and the model builder (expected figures for the example, blocking on an unfunded plan, warnings, input validation, workbook structure).
- The workbook's formulas were recalculated in LibreOffice and compared with the Python figures for all 36 months in both languages; the largest difference was 0.005, which is CSV rounding.
- CI runs all of the above on Python 3.9 and 3.12.

What has not been done: the skills have not yet been through structured evaluations with real founders across sectors, and the Arabic has been written natively but not reviewed by an independent editor. Reports of wording that reads wrong are welcome.

## Repository map

```
skills/        nine self-contained skills (SKILL.md, assets/, references/, scripts/)
context/       the seven layer templates and CLAUDE.md template, .en.md and .ar.md
templates/     canonical templates by area, .en.md and .ar.md
workflows/     four end-to-end workflows
frameworks/    competency framework, defensibility worksheet
examples/      worked example: context pack and financial model
shared/        scripts and glossary copied into the skills
tools/         sync_assets.py, validate.py, build_dist.py
tests/         unit tests for the scripts
```

Edit files in `templates/`, `context/` and `shared/`, then run `python tools/sync_assets.py` to refresh the copies inside each skill.

## Limits

This repository gives structure, method and checks. It does not give legal, tax, accounting or investment advice, and it does not know your market: the numbers and facts must come from you and your sources. Rules on company formation, fundraising instruments, data protection, marketing consent and employment differ by country and change; confirm them with a qualified adviser where you operate.

## Related repositories

Riyada stands on its own. Two sister repositories by the same author use it or complement it:

- [Saudi Agentic AI Entrepreneurship Academy](https://github.com/malenezi/saudi-agentic-ai-entrepreneurship-academy): an Arabic-first curriculum and Saudi market knowledge base. It maps Riyada's skills, templates and workflows to its four courses and adds [lab exercises](https://github.com/malenezi/saudi-agentic-ai-entrepreneurship-academy/tree/main/05-agentic-ai-lab/exercises) built on the context linter and the model builder. Rules specific to Saudi Arabia live there, not here. Its first two courses have full content, and two of Riyada's workflows run alongside them: *Idea to validated opportunity* with [Course 1](https://github.com/malenezi/saudi-agentic-ai-entrepreneurship-academy/blob/main/03-courses/01-opportunity/syllabus.md) and *First agent in 30 days* with [Course 2](https://github.com/malenezi/saudi-agentic-ai-entrepreneurship-academy/blob/main/03-courses/02-build/syllabus.md). See its [companion repositories page](https://github.com/malenezi/saudi-agentic-ai-entrepreneurship-academy/blob/main/07-resources/companion-repositories.md).
- [Bayan](https://github.com/malenezi/bayan): Arabic-first skills and linters for bilingual websites, HTML decks, RTL audits and interface text. Use it to build what the go-to-market and fundraising skills plan.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New templates, sector adaptations, corrections to Arabic or English wording, and reports from real use are all welcome.

## Licence

[MIT](LICENSE)

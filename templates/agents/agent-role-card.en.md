# Agent role card

One card per agent. Write it the way you would brief a capable new hire who has never seen the company.

- **Agent:** {{name}}
- **Owner:** {{the human accountable for its results}}
- **Version:** {{n}}, {{YYYY-MM-DD}}

## Purpose

{{One sentence: the outcome this agent exists to produce, and for whom.}}

## Goal and done criteria

- **Goal state:** {{what is true when a task is finished}}
- **Success measured by:** {{outcome metric, not activity}}
- **Not responsible for:** {{adjacent work that belongs to someone else}}

## Inputs and outputs

| | What | Format | From or to |
|---|---|---|---|
| Input | {{trigger or request}} | {{format}} | {{source}} |
| Output | {{deliverable}} | {{format}} | {{recipient}} |

## Context it reads

| Layer or document | When | Why |
|---|---|---|
| {{01 identity, 02 strategy}} | Always | {{reason}} |
| {{specific SOP or price list}} | {{when the task involves it}} | {{reason}} |

## Tools and permissions

Least privilege: grant only what the tasks need.

| Tool or system | Access | Limit |
|---|---|---|
| {{CRM}} | {{read / write}} | {{which objects, which fields}} |
| {{email}} | {{draft only / send}} | {{recipients, volume}} |

## Authority

- **May act alone on:** {{actions}}
- **Must propose and wait for:** {{actions and the approver}}
- **Must never:** {{actions}}
- **Budget per task:** {{tokens, money or minutes}}

## Handoffs and escalation

- **Hands off to:** {{agent or person, with what information}}
- **Escalates when:** {{conditions: low confidence, missing data, policy conflict, upset customer}}
- **Escalates to:** {{name and channel}}

## Evaluation

- **Eval rubric:** {{link}}
- **Pass rate required before autonomy increases:** {{%, over how many cases}}
- **Reviewed:** {{frequency and reviewer}}

## Known failure modes

| Failure | How it shows | Guard |
|---|---|---|
| {{e.g. invents a price}} | {{symptom}} | {{check, tool restriction or test case}} |

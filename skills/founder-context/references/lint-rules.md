# Context lint rules

`context_lint.py DIR` checks the files named `01-*.md` to `07-*.md` in `DIR`. If the folder holds language variants (`01-*.en.md`, `01-*.ar.md`), each language is checked as its own pack.

| Rule | Severity | Finds | Fix |
|---|---|---|---|
| CTX001 | error | A layer file is missing | Create it from the template |
| CTX002 | error | A `{{placeholder}}` was left unfilled | Fill it, or delete the line if it does not apply |
| CTX003 | error | A section has a heading and nothing under it | Write the content or remove the section |
| CTX004 | error | No valid `Last reviewed` date (ISO format) | Add `- **Last reviewed:** 2027-01-15` |
| CTX005 | warning | Not reviewed within the allowed age (90 days by default) | Review and update the date |
| CTX006 | warning | File is longer than the word limit (900 by default) | Move detail to a linked document |
| CTX007 | error | Layer 6 has no approval matrix | Add a table of actions with a level for each |
| CTX008 | error | Layer 6 has no "Never" rule | State at least one action agents must never take |
| CTX009 | error | The same `- **Field:** value` appears in two files with different values | Keep it in one file; point to it from the other |
| CTX010 | warning | A table cell is empty | Fill it or write "none" |
| CTX011 | error | Text that looks like a password, key or token | Remove it and rotate the secret |
| CTX012 | warning | TODO, TBD or FIXME left in the text | Resolve or move to Known gaps |
| CTX013 | error | Two files for the same layer | Merge them; one layer, one file |

## Options

| Option | Default | Use |
|---|---|---|
| `--max-age-days N` | 90 | Tighten for fast-moving teams |
| `--max-words N` | 900 | Raise only with a reason |
| `--strict` | off | Treat warnings as errors, for CI |
| `--format json` | text | Machine-readable output |
| `--today YYYY-MM-DD` | today | Fix the date for reproducible checks |

Exit status is 0 when clean, 1 when there are errors (or warnings with `--strict`), 2 on a usage error.

## What the linter cannot see

It checks form and consistency, not truth. It will not notice a wrong price, an approver who has left, or a procedure nobody follows. Those are caught by the test in the workflow (give an agent a real task) and by the review rhythm in layer 7.

## In continuous integration

```yaml
- run: python scripts/context_lint.py context/ --strict
```

A pack that fails the check should block changes to agent instructions that depend on it.

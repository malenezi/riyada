# Contributing · المساهمة

Contributions in Arabic or English are welcome. نرحب بالمساهمات بالعربية أو الإنجليزية.

## What helps most

- A template you use in a real venture that is missing here.
- A sector or country adaptation (for example, a services business, a marketplace, a regulated sector).
- Corrections to Arabic or English wording, especially terms that read as translated.
- A report from real use: what a skill got wrong, with the request that triggered it.
- New lint rules or model checks, with a test.

## How the repository is organised

Canonical files live in `templates/`, `context/` and `shared/`. Each skill carries copies under `assets/`, `scripts/` and `references/glossary.md` so that it works alone. Edit the canonical file, then run:

```bash
python tools/sync_assets.py
```

Never edit a copy inside `skills/*/assets` or `skills/*/scripts`; the next sync overwrites it.

## Rules for content

1. **Both languages, same structure.** Every `.en.md` has an `.ar.md` with the same headings, table rows and placeholders. Write each language natively; do not translate word for word. If you can only write one language, open the pull request and say so; a maintainer or another contributor can add the other.
2. **No invented facts.** No market statistics, benchmarks, company names, legal claims or customer quotes unless they are sourced in the text. Thresholds offered as rules of thumb are labelled as such.
3. **Fields, not prose.** Templates use `{{placeholders}}` that say what to write. Keep each template to what a founder would fill in one sitting.
4. **Human approval is explicit.** Anything that contacts a person, spends money or cannot be undone is marked for a human decision.
5. **Terms follow the glossary** in `shared/glossary.md`. Propose a change to the glossary if you think a term is wrong.
6. **Plain language.** Short sentences. No hype.

## Rules for skills

- Folder name equals the `name` in the frontmatter: lowercase letters, digits, hyphens.
- The description says what the skill does and when to use it ("Use when ..."), includes Arabic trigger terms, stays under 1,024 characters, and avoids `: ` (colon followed by a space).
- `SKILL.md` stays under 500 lines. Move depth into `references/`.
- Explain the reason behind an instruction. Avoid capital-letter commands.
- Scripts use the Python standard library where possible, document their exit codes, and come with tests.

## Before opening a pull request

```bash
python tools/sync_assets.py
python tools/validate.py
python -m unittest discover -s tests
```

All three must pass. CI runs the same checks on Python 3.9 and 3.12.

## Commit messages

Use a short imperative subject with a type prefix: `feat:`, `fix:`, `docs:`, `test:`, `chore:`. Example: `feat(templates): add partnership agreement checklist`.

## Licence

By contributing you agree that your contribution is released under the MIT licence of this repository.

.PHONY: sync check test dist example

sync:
	python tools/sync_assets.py

check: 
	python tools/sync_assets.py --check
	python tools/validate.py
	python shared/scripts/context_lint.py examples/mawja/context/en --today 2026-11-16
	python shared/scripts/context_lint.py examples/mawja/context/ar --today 2026-11-16

test:
	python -m unittest discover -s tests

dist:
	python tools/build_dist.py

example:
	python shared/scripts/build_model.py examples/mawja/assumptions.json --out examples/mawja/model.en --lang en
	python shared/scripts/build_model.py examples/mawja/assumptions.json --out examples/mawja/model.ar --lang ar

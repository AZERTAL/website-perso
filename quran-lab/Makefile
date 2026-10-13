.PHONY: all sync test lint fmt fetch db clean-db hooks reports
UV ?= uv

all: lint test db reports

sync:
	$(UV) sync

test:
	$(UV) run pytest -q

lint:
	$(UV) run ruff check .
	$(UV) run ruff format --check .

fmt:
	$(UV) run ruff format .

fetch:
	$(UV) run python scripts/fetch_sources.py

db:
	@if [ -z "$$(ls -A data/raw | grep -v .gitkeep)" ]; then \
	  echo "data/raw/ vide : sources non téléchargées (make fetch). Base non construite, aucun chiffre produit."; \
	else $(UV) run python scripts/build_db.py; fi

reports:
	@echo "Rapports : générés par quran_lab.cli (voir .claude/commands/verifie.md)"; $(UV) run python scripts/check_reports.py

hooks:
	git config core.hooksPath ../.githooks

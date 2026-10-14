.PHONY: all sync test lint fmt fetch db hooks reports audit h001 h001-v2 dataset site verify-sources help
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

hooks:  ## active le hook git de pré-commit (chemin relatif à la racine du dépôt)
	git config core.hooksPath .githooks

audit: db  ## audit des sources Tanzil -> reports/audit-tanzil.md et .json
	$(UV) run python scripts/audit_tanzil.py

h001: db  ## H001 : grille de règles niveau forme (exige un arbre git propre)
	$(UV) run python -m quran_lab.cli verifie "يوم" --target 365 --claim "le mot jour (يوم) apparaît 365 fois" --hypothesis H001 --out reports/H001-yawm-365.md

h001-v2: db  ## H001-v2 : espace de 512 spécifications
	$(UV) run python scripts/run_h001_v2.py

dataset: db  ## export CSV et Parquet dans data/processed/
	$(UV) run python scripts/export_dataset.py

site: audit  ## page de suivi (site/status.html)
	$(UV) run python scripts/build_status_page.py

verify-sources:  ## recalcule les SHA-256 de data/raw et compare à data/sources_manifest.json
	$(UV) run python scripts/verify_sources.py

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*## ' Makefile | sed 's/:.*## /\t/' 

#!/usr/bin/env bash
# Extrait Quran Lab (avec son historique) dans un dépôt dédié, sans toucher au portfolio.
# Usage : scripts/export_standalone_repo.sh /chemin/vers/nouveau-depot
#
# Prérequis : git-filter-repo (https://github.com/newren/git-filter-repo).
# Ne pousse rien : la création du dépôt distant et le `git push` restent à faire par le propriétaire.
set -euo pipefail

DEST="${1:?usage: $0 /chemin/vers/nouveau-depot}"
SRC="$(git rev-parse --show-toplevel)"

command -v git-filter-repo >/dev/null || { echo "git-filter-repo introuvable" >&2; exit 1; }
[ ! -e "$DEST" ] || { echo "$DEST existe déjà" >&2; exit 1; }

git clone --no-local "$SRC" "$DEST"
cd "$DEST"
# garde quran-lab/ (remonté à la racine), la configuration Claude Code, la CI et les gabarits
git filter-repo --force \
  --path quran-lab/ --path .claude/ --path .github/ --path .githooks/ --path CLAUDE.md --path .gitignore \
  --path-rename quran-lab/:
# adapte à la racine : chemins des hooks et de la configuration
sed -i 's#quran-lab/##g' CLAUDE.md .claude/settings.json
cat > .githooks/pre-commit <<'HOOK'
#!/bin/sh
# Activer avec : make hooks
python3 scripts/check_reports.py || exit 1
HOOK
chmod +x .githooks/pre-commit
sed -i 's#make hooks)#make hooks)#' README.md
cat > .github/workflows/quran-lab-ci.yml <<'CI'
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # check_reports lit l'historique git
      - uses: astral-sh/setup-uv@v5
      - run: uv sync
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run pytest -q
      - run: python3 scripts/check_reports.py
CI
git add -A && git -c user.name=export -c user.email=export@localhost commit -qm "Adaptation des chemins pour un dépôt dédié"
echo "Dépôt extrait dans $DEST. Relire CLAUDE.md, .claude/settings.json et la CI, lancer 'make test', puis :"
echo "  git remote add origin <url> && git push -u origin main"

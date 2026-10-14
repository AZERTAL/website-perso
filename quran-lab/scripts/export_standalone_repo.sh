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
# adapte les chemins qui supposaient quran-lab/ à la racine
sed -i 's#quran-lab/##g' CLAUDE.md .githooks/pre-commit .claude/settings.json 2>/dev/null || true
sed -i '/working-directory: quran-lab/,+0d; /defaults:/,/working-directory/d; s#quran-lab/\*\*#**#g' .github/workflows/quran-lab-ci.yml 2>/dev/null || true
echo "Dépôt extrait dans $DEST. Relire CLAUDE.md, .claude/settings.json et la CI, lancer 'make test', puis :"
echo "  git remote add origin <url> && git push -u origin main"

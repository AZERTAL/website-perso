"""Garde-fous des hooks Claude Code. Bibliothèque standard uniquement, logique pure.

Limite assumée : on bloque les verbes shell qui modifient `data/raw/` (redirections, rm, mv,
cp, chmod, sed -i, tee, touch, ln, truncate, dd). Un script Python qui écrirait dans ce
dossier n'est pas détecté ici ; la défense en profondeur est `chmod a-w` après téléchargement.
"""

from __future__ import annotations

import os
import re

RAW = "quran-lab/data/raw"
FETCH = "scripts/fetch_sources.py"
_MUTATING = re.compile(
    r"(>>?\s*\S*data/raw)|(\b(rm|mv|cp|chmod|chown|tee|touch|ln|truncate|dd|install|rsync)\b)"
    r"|(\bsed\s+(-\w*i|--in-place))"
)


def _is_raw_path(file_path: str, cwd: str) -> bool:
    p = file_path if os.path.isabs(file_path) else os.path.join(cwd, file_path)
    q = os.path.normpath(p) + "/"
    if f"/{RAW}/" in q:
        return True
    # Projet extrait à la racine d'un dépôt dédié : le dossier est reconnu à la présence de
    # scripts/fetch_sources.py dans le dossier parent de data/raw.
    if "/data/raw/" in q:
        root = q.split("/data/raw/")[0]
        return os.path.exists(os.path.join(root, "scripts", "fetch_sources.py"))
    return False


def decide(payload: dict) -> str | None:
    """Renvoie un message de refus, ou None si l'appel est autorisé."""
    tool = payload.get("tool_name", "")
    inp = payload.get("tool_input", {}) or {}
    cwd = payload.get("cwd") or os.getcwd()
    if tool in {"Write", "Edit", "MultiEdit", "NotebookEdit"}:
        fp = inp.get("file_path") or inp.get("notebook_path") or ""
        if fp and _is_raw_path(fp, cwd):
            return f"REFUSÉ : {RAW}/ est en lecture seule (sources brutes). Utiliser {FETCH}."
    if tool == "Bash":
        cmd = inp.get("command", "")
        if "data/raw" in cmd and "fetch_sources.py" not in cmd and _MUTATING.search(cmd):
            return f"REFUSÉ : commande susceptible de modifier {RAW}/. Utiliser {FETCH}."
    return None


def is_commit(payload: dict) -> bool:
    if payload.get("tool_name") != "Bash":
        return False
    cmd = (payload.get("tool_input") or {}).get("command", "")
    return bool(re.search(r"\bgit\b[^|;&]*\bcommit\b", cmd))

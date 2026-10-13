import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "fetch_sources", Path(__file__).resolve().parents[2] / "scripts" / "fetch_sources.py"
)
fs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fs)

ROW = {
    "id": "a",
    "dest": "a.txt",
    "url": "u",
    "date": "2026-10-13",
    "sha256": "ab",
    "license_note": "l",
}


def test_upsert_is_idempotent_and_preserves_surrounding_text():
    md = "# Sources\nintro\n"
    once = fs.upsert_table(md, fs.sources_table([ROW]))
    twice = fs.upsert_table(once, fs.sources_table([ROW]))
    assert once == twice
    assert once.startswith("# Sources\nintro")
    assert once.count(fs.BEGIN) == 1


def test_sources_with_null_url_are_listed_for_manual_resolution():
    import yaml

    cfg = yaml.safe_load(
        (Path(__file__).resolve().parents[2] / "config" / "sources.yaml").read_text(
            encoding="utf-8"
        )
    )
    nulls = [s["id"] for s in cfg["sources"] if not s.get("url")]
    # la morphologie exige une adresse e-mail sur le site : son URL n'est PAS devinée
    assert "qac_morphology_v04" in nulls
    assert "tanzil_uthmani" not in nulls


def test_merge_rows_keeps_other_sources_when_only_one_is_refetched():
    a = {**ROW, "id": "a"}
    b = {**ROW, "id": "b", "sha256": "bb"}
    merged = fs.merge_rows([a, b], [{**a, "sha256": "new"}])
    assert [r["id"] for r in merged] == ["a", "b"]
    assert merged[0]["sha256"] == "new" and merged[1]["sha256"] == "bb"

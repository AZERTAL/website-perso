from quran_lab.guards import decide, is_commit

CWD = "/home/user/website-perso"


def w(tool, **inp):
    return {"tool_name": tool, "tool_input": inp, "cwd": CWD}


def test_write_in_raw_is_refused():
    assert decide(w("Write", file_path=f"{CWD}/quran-lab/data/raw/x.txt"))
    assert decide(w("Edit", file_path="quran-lab/data/raw/x.txt"))
    assert decide(w("Write", file_path=f"{CWD}/quran-lab/data/raw/../raw/x.txt"))


def test_write_elsewhere_is_allowed():
    assert decide(w("Write", file_path=f"{CWD}/quran-lab/data/processed/x.csv")) is None
    assert decide(w("Write", file_path=f"{CWD}/quran-lab/data/rawish/x")) is None


def test_relative_path_from_lab_cwd():
    p = {"tool_name": "Write", "tool_input": {"file_path": "data/raw/a"}, "cwd": f"{CWD}/quran-lab"}
    assert decide(p)


def test_bash_mutations_of_raw_refused():
    for cmd in [
        "rm quran-lab/data/raw/a",
        "echo x > quran-lab/data/raw/a",
        "mv a data/raw/b",
        "sed -i s/a/b/ data/raw/a",
        "chmod 777 data/raw",
        "cp x data/raw/",
    ]:
        assert decide(w("Bash", command=cmd)), cmd


def test_bash_reads_of_raw_allowed():
    for cmd in [
        "cat data/raw/a | head",
        "sha256sum data/raw/*",
        "ls -la data/raw",
        "wc -l data/raw/a",
    ]:
        assert decide(w("Bash", command=cmd)) is None, cmd


def test_fetch_script_is_the_only_writer():
    assert (
        decide(w("Bash", command="uv run python scripts/fetch_sources.py && chmod -R a-w data/raw"))
        is None
    )


def test_is_commit():
    assert is_commit(w("Bash", command='git commit -m "x"'))
    assert is_commit(w("Bash", command="git add -A && git commit -m x"))
    assert not is_commit(w("Bash", command="git status"))
    assert not is_commit(w("Write", file_path="a"))


def test_standalone_layout_is_recognised_by_the_fetch_script(tmp_path):
    proj, other = tmp_path / "proj", tmp_path / "other"
    (proj / "scripts").mkdir(parents=True)
    (proj / "scripts" / "fetch_sources.py").write_text("")
    payload = {
        "tool_name": "Write",
        "tool_input": {"file_path": str(proj / "data/raw/x")},
        "cwd": str(proj),
    }
    assert decide(payload)
    payload["tool_input"]["file_path"] = str(other / "data/raw/x")
    assert decide(payload) is None  # un autre dossier « data/raw » n'est pas protégé

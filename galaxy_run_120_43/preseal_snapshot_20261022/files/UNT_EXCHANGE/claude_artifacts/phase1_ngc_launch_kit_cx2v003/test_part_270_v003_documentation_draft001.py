"""Disclosure checks on the immutable text included verbatim in the release README."""


V003_DOC_SHA256 = "b3210f66c1913b22f1ff56e3186a010002f53d7c029323d0618869a39dc522f9"


def v003_documentation_check(text):
    required = (
        "Work logs are guard-read only.",
        "Work logs are not checked for realpath equality.",
        "The sampler no longer raises MULTIPLE_MONITORS.",
        "the existing refusal for multiple exact live matches remains outside the sampler.",
        "Pinned executables are hashed in the parent, then executed by path in child processes.",
    )
    for sentence in required:
        if sentence not in text:
            raise AssertionError("missing or changed disclosure: " + sentence)


def v003_documentation_cases(suite):
    from pathlib import Path
    def action():
        path = Path(__file__).parent / "README_CONTRACT_CX2V003.md"
        raw = path.read_bytes()
        suite.eq(suite.module.sha(raw), V003_DOC_SHA256)
        v003_documentation_check(raw.decode())
        suite.interfaces["cx2v003_readme_contract"] = {
            "path": str(path), "sha256": V003_DOC_SHA256,
            "release_rule": "The final README must contain these exact bytes as a contiguous section.",
        }
    suite.case("CX2V003_A09_and_V1_documentation", action)


def v003_documentation_mutants(suite):
    from pathlib import Path
    raw = (Path(__file__).parent / "README_CONTRACT_CX2V003.md").read_bytes()
    text = raw.decode()
    rows = []
    for name, old, new in (
        ("A09_restore_blanket_realpath_claim", "Work logs are guard-read only.",
         "Every work log requires realpath equality."),
        ("V1_hide_MULTIPLE_MONITORS_change", "The sampler no longer raises MULTIPLE_MONITORS.",
         "Sampler behavior is unchanged."),
    ):
        def action(name=name, old=old, new=new):
            v003_documentation_check(text)
            suite.eq(text.count(old), 1)
            changed = text.replace(old, new)
            try:
                v003_documentation_check(changed)
            except AssertionError:
                rows.append({"name": name, "control": "PASS", "status": "KILLED",
                             "kind": "documentation", "source_sha256": suite.module.sha(changed.encode()),
                             "replace": old, "with": new})
            else:
                raise AssertionError("documentation mutant survived")
        suite.case("CX2V003_MUTANT_" + name, action)
    suite.interfaces["cx2v003_documentation_mutants"] = rows

# Codex2 independent r10 H07 review

date -u: Sun Oct 18 17:09:30 UTC 2026

TESTED: 18 owned-surrogate predicates, 17 satisfied. Candidate source e801adc4 is unchanged. This component reports one SHOULD_FIX and one coordinator policy decision; it is not a whole-compare verdict.

The path guard refuses the owned registered directory, its files and nonexistent descendants, symlink aliases, file hard links, lexical /.vol directory/file names and the available same-inode firmlink alias. read_run refuses the linked result before any open, and refuses a protected side path after reading only the ordinary result. A plain owned run passes the bounded read control. No protected actual run or target was stat-ed, listed or opened. The test replaces registered root/name constants with owned paths before calling the guard, and uses a minimal adapter only for the read_run control. These seams do not establish scientific validity or full CLI adoption.

**CX2-R10-H07-S1, SHOULD_FIX: unavailable registered-root identity disables hard-link protection.** _registered_run_identities catches OSError and silently omits the failed root. With a fault-injected PermissionError on the owned registered-root stat, c5h_path_hit returns False for an existing hard link to an owned protected file. No content is opened by this unit probe. Actual production occurrence and the full CLI consequence are UNTESTED. A guard claiming fail-closed hard-link protection should propagate inability to obtain the required registered identity and refuse the attempted read, rather than interpreting the empty device set as safe.

**Policy decision, BUILD NEW-64:** the implementation refuses every multiply-linked regular file on a registered device, including unrelated files. The owned unrelated-hardlink control confirms that conservative behavior. A75.4 asks for identity against every protected file, whereas this code uses a superset without enumerating the actual run. Claude2 must accept that declared substitute or supply its own authorized inode inventory. This review has no authority to inventory the protected run.

The /.vol checks are lexical rejection tests only; no /.vol target was accessed. The fixture contains only synthetic tiny JSON files. No launches, network, session logs, git writes, deletion, moves or overwrites. Approved isolated Python and single-thread environment with the 0514 nice waiver. The audit/metadata guard recorded zero forbidden operations.

## Cited byte pins

- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r10/kmax_tail_compare_c2v007_r10.py`
  sha256 `e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/h07/probe_h07_cx2v001.py`
  sha256 `876c8667073bdee86196978f39e09bf84b3c6e04caeb15cddd65204bc533052e`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/h07/H07_RESULTS_CX2V001.json`
  sha256 `d4d344468c1a3ab8394b5ea5fcb69491c79a3868eb2227a384fcf305321b4ade`
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_v007_compare_final_cx2/OPEN_RULINGS_SNAPSHOT_CX2V001.md`
  sha256 `2da736b5f4f8f6c007035996218f98838c2766b4a4daf11ca62ab3d3ec254827`

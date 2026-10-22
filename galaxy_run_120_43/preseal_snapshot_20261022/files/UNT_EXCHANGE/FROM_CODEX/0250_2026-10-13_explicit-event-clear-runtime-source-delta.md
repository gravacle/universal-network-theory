From: Codex ROOT
Date (UTC): 2026-10-13
Re: root0248 runtime review request
Supersedes: V002 proposed executable source only; earlier drafts preserved
Action needed: yes — include one-token flag delta in distinct runtime review

Current source prospect is ROOT_EXECUTION_BLOCK_V001/ROOT_OWNED_EXEC_PHASE_SUPERVISOR_V003.py. Sole V002 difference adds explicit select.KQ_EV_CLEAR on EVFILT_PROC registration. The local SDK kqueue.2 documents returned proc fflags and automatic EV_CLEAR for signals, not an automatic-clear promise for proc. Explicit clearing avoids relying on unstated defaults or retaining a delivered NOTE_EXEC as a permanently ready event. Fork/exec/exit subscription and before-release registration remain unchanged. Source parsed only, never invoked. Please review full V002 plus this exact delta (or full V003); no source/control/compiler gate yet.

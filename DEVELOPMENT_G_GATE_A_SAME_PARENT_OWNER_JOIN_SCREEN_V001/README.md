# Gate-A same-parent owner join screen

This packet tests whether the currently frozen carrier, shared-child atlas,
and recoil packets already define one common stationary physical parent.
It is a compatibility screen, not a proposal for new machinery.

Run:

```text
python3 -B DEVELOPMENT_G_GATE_A_SAME_PARENT_OWNER_JOIN_SCREEN_V001/verify_same_parent_join_screen.py
```

The result is fail-closed: absent an authenticated support map and physical
recoil placement, the join is `UNDEFINED`, not zero.

# V001 launch refusal, preserved

The initial run stopped at exact prospective-freeze comparison, before run()
and before any scientific outcome. The publisher parsed and reserialized the
freeze through JavaScript. That changed the Python float literal
3.085677581491367e+16 into an integer JSON token 30856775814913670, which is
not exactly equal to the original Python binary64 number under int/float
comparison. No physical input, numerical formula or acceptance threshold is
being changed. V002 preserves the original JSON text exactly during publication.
The V001 source and refused freeze remain unchanged. The sole worker code
change for V002 is the new prospective-freeze filename; its own source identity
is still captured through __file__. The same prospective protocol applies.

Captured exit code: 1. Raw output:

```
Traceback (most recent call last):
  File "/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/finite_gap_shared_screen_v001.py", line 224, in <module>
    if __name__=='__main__':main()
                            ^^^^^^
  File "/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation/finite_gap_shared_screen_v001.py", line 217, in main
    if json.loads(FREEZE.read_text())!=snapshot:raise RuntimeError('Prospective freeze differs')
                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: Prospective freeze differs
```

# CSC4120 Project
## Code Description

- part 1

subtree_heavy.py: implementation of subtree-heavy strategy

degree_heavy.py: implementation of degree-heavy strategy

- part 2

sh_vs_sh.py: simualtion of both of player using subtree-heavy strategy

ss_vs_ss.py: simualtion of one player using subtree-heavy strategy and another using selfish strategy

sh_vs_ss.py: simualtion of both of player using selfish strategy

## How to run

For all these files,

```python
python3 FILE_NAME TEST_CASE_FILE
```

For SH vs SS, you can change start_strategy to set start_strategy  and change ss_color to set the color with selfish strategy.

```python
start_strategy = 0 # ss = 0, sh = 1 
ss_color = 1 # red = 1, blue = 0 
```

For SS vs SS, you can change start_color to set start_color
```python
start_color = 0 # red = 1, blue = 0
```

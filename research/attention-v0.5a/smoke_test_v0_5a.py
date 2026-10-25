from importlib.metadata import version
import numpy as np
from cadence import Brain

assert version("cadence-net") == "0.88.0", version("cadence-net")

brain = Brain.compose(
    inputs=12,
    actions=3,
    modules=(64,),
    learned_code=16,
    attention=True,
    recall_heads=2,
    recall_address=0.01,
    recall_temperature=0.25,
    episodic=False,
    teaching="normalized",
    learning_qualified=True,
    learning_damping=3,
    learning_free_steps=1024,
    learning_nudged_steps=1024,
    learning_tolerance=0.003,
    seed=9951,
)

assert brain.recall is not None
assert brain.recall.heads == 2
assert len(brain.recall.head_maps) == 1
assert len(brain.recall.head_map(0)) == 3
assert len(brain.recall.head_map(1)) == 3
assert brain.learned_code is not None

x = np.zeros((1, 12), dtype=float)
x[0, 0] = 1.0
brain.act(x, greedy=True)

trial = __import__("copy").deepcopy(brain)
w_x, w_c, b = trial.recall.head_map(0)
trial.recall.head_maps[0] = (w_x.copy(), w_c.copy(), b.copy())
assert all(
    np.array_equal(a, b)
    for a, b in zip(trial.recall.head_map(0), trial.recall.head_map(1))
)

print("V0.5A Cadence 0.88.0 multi-head attention smoke test: PASSED")
print("recall heads:", brain.recall.heads)
print("learned code units:", 16)

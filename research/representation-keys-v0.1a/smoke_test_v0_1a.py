from importlib.metadata import version
from pathlib import Path
import tempfile
import numpy as np
from cadence import Brain

assert version("cadence-net") == "0.84.3", version("cadence-net")

x = np.zeros((4, 36), dtype=float)
for i in range(4):
    x[i, i] = 1.0
    x[i, 4:] = np.linspace(-0.2, 0.2, 32) * (1 if i % 2 == 0 else -1)
y = np.arange(4, dtype=int)

brain = Brain.compose(inputs=36, actions=4, modules=(24, 12), seed=909, recall=False)
brain.reset()
report = brain.lesson(x, y)
assert isinstance(report, dict)

brain.reset()
a = np.asarray(brain.act(x[[0]], greedy=True)).reshape(-1)
assert a.shape == (1,)
state = brain.basal_ganglia.state
assert state is not None
idx = np.asarray(brain.association_index, dtype=int)
key = np.asarray(state.activation[0, idx], dtype=float)
assert key.shape == (12,) and np.isfinite(key).all()

code_brain = Brain.compose(inputs=36, actions=4, modules=(24, 12), code=128, seed=909, recall=False)
code = np.asarray(code_brain.observation_code(x[[0]]), dtype=float)
assert code.shape == (1, 128) and np.isfinite(code).all() and np.linalg.norm(code) > 0

with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / "brain.npz"
    brain.save(p)
    copy = Brain.load(p)
    copy.reset()
    copy.act(x[[0]], greedy=True)
    state2 = copy.basal_ganglia.state
    assert state2 is not None
    key2 = np.asarray(state2.activation[0, np.asarray(copy.association_index, dtype=int)], dtype=float)
    assert key2.shape == (12,) and np.isfinite(key2).all()

print("Representation Keys V0.1A association-state + lesson + fixed-code + save/load smoke test: PASSED")

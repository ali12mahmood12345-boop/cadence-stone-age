
from importlib.metadata import version
import numpy as np
from cadence import Brain

print("cadence-net:", version("cadence-net"))

assert version("cadence-net") == "0.81.0"
assert hasattr(Brain, "wait")

brain = Brain.compose(
    inputs=4,
    actions=2,
    modules=(8,),
    seed=1,
    arousal=True,
)

obs = np.asarray(
    [[1.0, 0.0, 0.0, 0.0]],
    dtype=np.float64,
)

later = np.asarray(
    [[0.9, 0.1, 0.0, 0.0]],
    dtype=np.float64,
)

brain.live(obs)
owner = brain.decision_id

brain.wait(later)

brain.live(
    obs,
    reward=np.asarray(
        [0.0],
        dtype=np.float64,
    ),
    done=np.asarray(
        [True],
        dtype=bool,
    ),
    decision_id=owner,
)

print("Brain.wait smoke test: PASSED")

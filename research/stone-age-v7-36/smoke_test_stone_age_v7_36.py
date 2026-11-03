from importlib.metadata import version as pkg_version
import numpy as np
import stone_age_v7_36_position_convergence as v

assert pkg_version("cadence-net") == v.VERSION
assert len(v.PAIRS) == 22
assert v.CHECKPOINTS == (198, 396, 792)
assert sum(v.STAGE_PER_PAIR) == 792
assert v.LEARNING_FREE_STEPS == 4096

brain = v.compose(73636)
assert int(brain.learner.config.free_steps) == v.LEARNING_FREE_STEPS
state = {"episode": None, "teacher_rows": 0, "teacher_correct": 0}
v.install_exact_position_teacher(brain, state)
mini = v._make_panel(73636, 99, 1)
assert len(mini) == 22
tr = v.train_stage(brain, mini, state)
assert tr["lessons"] == 22 and not tr["runtime_errors"], tr
assert state["teacher_rows"] == 22 and state["teacher_correct"] == 22, state
assert float(np.max(np.abs(np.asarray(brain.recall.position_c)))) <= 1e-12
assert v._address_map_max_abs(brain) <= 1e-12
geom, rows = v.position_map_geometry(brain, "SMOKE")
assert len(rows) == 22 and 0.0 <= geom["top_predecessor_rate"] <= 1.0
# Verify the test-only predecessor oracle executes on an exact-balanced mini panel.
rr, _ = v.eval_condition(brain, mini, "FORCE_PREDECESSOR", "SMOKE", panel="SMOKE")
assert rr["valid"] == 1 and rr["tests"]["total"] == 22, rr
print("V7.36 FIXED smoke test passed: 4096 free-step budget, exact teacher, frozen address/P_c, cumulative-dose harness, map geometry, and predecessor oracle execute.")


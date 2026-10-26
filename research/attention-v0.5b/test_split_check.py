from split_check import report, split_v05a, split_v05b


def test_v05a_split_cannot_test_generalization():
    r = report("V0.5A", *split_v05a(), 6)
    assert r["held_pairs_determined"] == 0 and not r["tests_conjunctive_generalization"]


def test_v05b_split_is_balanced_and_identifiable():
    r = report("V0.5B", *split_v05b(), 9)
    assert r["single_fact_chance_taught"] and r["single_fact_chance_held"]
    assert r["held_pairs_determined"] == r["held_pairs"] == 27
    assert r["tests_conjunctive_generalization"]

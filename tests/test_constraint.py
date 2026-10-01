from csdr.constraint import evidence_is_sufficient


def test_sufficient_evidence():
    assert evidence_is_sufficient(0.85) is True


def test_insufficient_evidence():
    assert evidence_is_sufficient(0.40) is False


def test_exact_default_threshold():
    assert evidence_is_sufficient(0.72) is True


def test_just_below_default_threshold():
    assert evidence_is_sufficient(0.719) is False


def test_custom_threshold():
    assert evidence_is_sufficient(0.60, threshold=0.50) is True
    assert evidence_is_sufficient(0.40, threshold=0.50) is False


def test_zero_score():
    assert evidence_is_sufficient(0.0) is False


def test_perfect_score():
    assert evidence_is_sufficient(1.0) is True


def test_low_threshold_for_tf_idf():
    assert evidence_is_sufficient(0.25, threshold=0.25) is True
    assert evidence_is_sufficient(0.15, threshold=0.25) is False

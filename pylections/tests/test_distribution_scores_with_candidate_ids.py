from pylections.distribution.distribution import Distribution, CandidateDoesNotExistError
import pytest


""" Test adding candidates and scores to distributions using candidate IDs """


def test_add_single_candidate() -> None:
    """ Test that we can add a single candidate and that its score can be accessed correctly. """
    d = Distribution(1)
    d.add_score("candidate_id", 10)

    score, awarded_seats = d["candidate_id"]
    assert score == 10
    assert awarded_seats == -1


def test_set_score_of_candidate() -> None:
    """ Test that we can set the score of a single candidate and that its score can be accessed correctly. """
    d = Distribution(1)
    d.set_score("candidate_id", 5)

    score, awarded_seats = d["candidate_id"]
    assert score == 5
    assert awarded_seats == -1


def test_add_score_to_existing_candidate() -> None:
    """ Test that we can add a single candidate and that its score can be accessed correctly.
    Then test that we can add more score to the candidate and get the correct result.
    """
    d = Distribution(1)
    d.add_score("candidate_id", 10)

    score, awarded_seats = d["candidate_id"]
    assert score == 10
    assert awarded_seats == -1

    d.add_score("candidate_id", 10)

    score, awarded_seats = d["candidate_id"]
    assert score == 20
    assert awarded_seats == -1


def test_set_score_of_existing_candidate() -> None:
    """ Test that we can set the score of a single candidate and that its score can be accessed correctly.
    Then test that we can set the score again to a new value.
    """
    d = Distribution(1)
    d.add_score("candidate_id", 10)

    score, awarded_seats = d["candidate_id"]
    assert score == 10
    assert awarded_seats == -1

    d.set_score("candidate_id", 5)

    score, awarded_seats = d["candidate_id"]
    assert score == 5
    assert awarded_seats == -1


def test_add_multiple_candidates() -> None:
    """ Test that we can add multiple candidates and that their scores are all correct. """
    d = Distribution(1)
    d.add_score("candidate_id_1", 10)
    d.add_score("candidate_id_2", 42)

    score, awarded_seats = d["candidate_id_1"]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d["candidate_id_2"]
    assert score == 42
    assert awarded_seats == -1


def test_set_multiple_candidates() -> None:
    """ Test that we can add multiple candidates, and then set each of their scores to a new value. """
    d = Distribution(1)
    d.add_score("candidate_id_1", 10)
    d.add_score("candidate_id_2", 42)

    d.set_score("candidate_id_1", 13)
    d.set_score("candidate_id_2", 27)

    score, awarded_seats = d["candidate_id_1"]
    assert score == 13
    assert awarded_seats == -1

    score, awarded_seats = d["candidate_id_2"]
    assert score == 27
    assert awarded_seats == -1


def test_add_multiple_candidates_list() -> None:
    """ Test that we can add candidates by passing lists of candidates and scores to the add_score method. """
    d = Distribution(1)

    candidates = ["cand1", "cand2", "cand3"]
    scores = [42, 10, 13]

    d.add_score(candidates, scores)

    score, awarded_seats = d["cand1"]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 13
    assert awarded_seats == -1


def test_add_more_to_multiple_candidates_list() -> None:
    """ Test that we can add more score to candidates using lists of IDs and scores. """
    d = Distribution(1)

    candidates = ["cand1", "cand2", "cand3"]
    scores = [42, 10, 13]

    d.add_score(candidates, scores)

    score, awarded_seats = d["cand1"]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 13
    assert awarded_seats == -1

    candidates_to_add_to = ["cand1", "cand3"]
    scores = [5, 11]
    d.add_score(candidates_to_add_to, scores)

    score, awarded_seats = d["cand1"]
    assert score == 47
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10 # cand2 should not change
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 24
    assert awarded_seats == -1


def test_set_to_multiple_candidates_list() -> None:
    """ Test that we can set the score of candidates using lists of IDs and scores. """
    d = Distribution(1)

    candidates = ["cand1", "cand2", "cand3"]
    scores = [42, 10, 13]

    d.add_score(candidates, scores)

    score, awarded_seats = d["cand1"]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 13
    assert awarded_seats == -1

    candidates_to_set = ["cand1", "cand3"]
    scores = [5, 11]
    d.set_score(candidates_to_set, scores)

    score, awarded_seats = d["cand1"]
    assert score == 5
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10 # cand2 should not change
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 11
    assert awarded_seats == -1


def test_add_multiple_candidates_tuple() -> None:
    """ Test that we can add candidates by passing tuples of candidates and scores to the add_score method. """
    d = Distribution(1)

    candidates = ("cand1", "cand2", "cand3")
    scores = (42, 10, 13)

    d.add_score(candidates, scores)

    score, awarded_seats = d["cand1"]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 13
    assert awarded_seats == -1


def test_add_more_to_multiple_candidates_tuple() -> None:
    """ Test that we can add more score to candidates using tuples of IDs and scores. """
    d = Distribution(1)

    candidates = ("cand1", "cand2", "cand3")
    scores = (42, 10, 13)

    d.add_score(candidates, scores)

    score, awarded_seats = d["cand1"]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 13
    assert awarded_seats == -1

    candidates_to_add_to = ("cand1", "cand3")
    scores = (5, 11)
    d.add_score(candidates_to_add_to, scores)

    score, awarded_seats = d["cand1"]
    assert score == 47
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10 # cand2 should not change
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 24
    assert awarded_seats == -1


def test_set_to_multiple_candidates_tuple() -> None:
    """ Test that we can set the score of candidates using tuples of IDs and scores. """
    d = Distribution(1)

    candidates = ("cand1", "cand2", "cand3")
    scores = (42, 10, 13)

    d.add_score(candidates, scores)

    score, awarded_seats = d["cand1"]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 13
    assert awarded_seats == -1

    candidates_to_set = ("cand1", "cand3")
    scores = (5, 11)
    d.set_score(candidates_to_set, scores)

    score, awarded_seats = d["cand1"]
    assert score == 5
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10 # cand2 should not change
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 11
    assert awarded_seats == -1


def test_add_multiple_candidates_dict() -> None:
    """ Test that we can add candidates by passing a dictionary with candidates and scores to the add_score method. """
    d = Distribution(1)

    candidates = {
        "cand1": 42,
        "cand2": 10,
        "cand3": 13
    }

    d.add_score(candidates)

    score, awarded_seats = d["cand1"]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 13
    assert awarded_seats == -1


def test_add_more_to_multiple_candidates_dict() -> None:
    """ Test that we can add more score to candidates using a dictionary of IDs and scores. """
    d = Distribution(1)

    candidates = {
        "cand1": 42,
        "cand2": 10,
        "cand3": 13
    }

    d.add_score(candidates)

    score, awarded_seats = d["cand1"]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 13
    assert awarded_seats == -1

    candidates_to_add_to = {
        "cand1": 5,
        "cand3": 11
    }
    d.add_score(candidates_to_add_to)

    score, awarded_seats = d["cand1"]
    assert score == 47
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10 # cand2 should not change
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 24
    assert awarded_seats == -1


def test_set_to_multiple_candidates_dict() -> None:
    """ Test that we can set the score of candidates using a dictionary of IDs and scores. """
    d = Distribution(1)

    candidates = {
        "cand1": 42,
        "cand2": 10,
        "cand3": 13
    }

    d.add_score(candidates)

    score, awarded_seats = d["cand1"]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 13
    assert awarded_seats == -1

    candidates_to_set = {
        "cand1": 5,
        "cand3": 11
    }
    d.set_score(candidates_to_set)

    score, awarded_seats = d["cand1"]
    assert score == 5
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 10 # cand2 should not change
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 11
    assert awarded_seats == -1


def test_CandidateDoesNotExistError() -> None:
    """ Test that we get a CandidateDoesNotExistError if trying to access the score of a candidate
    which does not exist, or if we try to remove a candidate which does not exist.
    """
    d = Distribution(1)
    d.add_score("cand1", 10)

    with pytest.raises(CandidateDoesNotExistError):
        d.remove_candidate("cand2")

    with pytest.raises(CandidateDoesNotExistError):
        score, awarded_seats = d["cand2"]

    score, awarded_seats = d["cand1"]
    assert score == 10
    assert awarded_seats == -1


def test_remove_candidate() -> None:
    """ Test that we can add and remove a candidate without affecting other candidates. """
    d = Distribution(1)
    d.add_score(["cand1", "cand2", "cand3"], [5, 7, 11])

    score, awarded_seats = d["cand1"]
    assert score == 5
    assert awarded_seats == -1

    score, awarded_seats = d["cand2"]
    assert score == 7
    assert awarded_seats == -1

    score, awarded_seats = d["cand3"]
    assert score == 11
    assert awarded_seats == -1

    d.remove_candidate("cand2")

    score, awarded_seats = d["cand1"]
    assert score == 5
    assert awarded_seats == -1

    with pytest.raises(CandidateDoesNotExistError):
        score, awarded_seats = d["cand2"] # should get a CandidateDoesNotExistError on this now.

    score, awarded_seats = d["cand3"]
    assert score == 11
    assert awarded_seats == -1

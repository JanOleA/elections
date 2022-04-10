from elections.distribution.distribution import Distribution, CandidateDoesNotExistError, Party
import pytest


""" Test adding candidates and scores to distributions using Party objects """
bears = Party("Bears")
foxes = Party("Foxes")
cats = Party("Cats")
dogs = Party("Dogs")


def test_add_single_candidate() -> None:
    """ Test that we can add a single candidate and that its score can be accessed correctly. """
    d = Distribution(1)
    d.add_score(bears, 10)

    score, awarded_seats = d[bears]
    assert score == 10
    assert awarded_seats == -1


def test_set_score_of_candidate() -> None:
    """ Test that we can set the score of a single candidate and that its score can be accessed correctly. """
    d = Distribution(1)
    d.set_score(foxes, 5)

    score, awarded_seats = d[foxes]
    assert score == 5
    assert awarded_seats == -1


def test_add_score_to_existing_candidate() -> None:
    """ Test that we can add a single candidate and that its score can be accessed correctly.
    Then test that we can add more score to the candidate and get the correct result.
    """
    d = Distribution(1)
    d.add_score(cats, 10)

    score, awarded_seats = d[cats]
    assert score == 10
    assert awarded_seats == -1

    d.add_score(cats, 10)

    score, awarded_seats = d[cats]
    assert score == 20
    assert awarded_seats == -1


def test_set_score_of_existing_candidate() -> None:
    """ Test that we can set the score of a single candidate and that its score can be accessed correctly.
    Then test that we can set the score again to a new value.
    """
    d = Distribution(1)
    d.add_score(dogs, 10)

    score, awarded_seats = d[dogs]
    assert score == 10
    assert awarded_seats == -1

    d.set_score(dogs, 5)

    score, awarded_seats = d[dogs]
    assert score == 5
    assert awarded_seats == -1


def test_add_multiple_candidates() -> None:
    """ Test that we can add multiple candidates and that their scores are all correct. """
    d = Distribution(1)
    d.add_score(dogs, 10)
    d.add_score(cats, 42)

    score, awarded_seats = d[dogs]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d[cats]
    assert score == 42
    assert awarded_seats == -1


def test_set_multiple_candidates() -> None:
    """ Test that we can add multiple candidates, and then set each of their scores to a new value. """
    d = Distribution(1)
    d.add_score(bears, 10)
    d.add_score(foxes, 42)

    d.set_score(bears, 13)
    d.set_score(foxes, 27)

    score, awarded_seats = d[bears]
    assert score == 13
    assert awarded_seats == -1

    score, awarded_seats = d[foxes]
    assert score == 27
    assert awarded_seats == -1


def test_add_multiple_candidates_list() -> None:
    """ Test that we can add candidates by passing lists of candidates and scores to the add_score method. """
    d = Distribution(1)

    candidates = [cats, bears, foxes]
    scores = [42, 10, 13]

    d.add_score(candidates, scores)

    score, awarded_seats = d[cats]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d[foxes]
    assert score == 13
    assert awarded_seats == -1


def test_add_more_to_multiple_candidates_list() -> None:
    """ Test that we can add more score to candidates using lists of parties and scores. """
    d = Distribution(1)

    candidates = [cats, bears, foxes]
    scores = [42, 10, 13]

    d.add_score(candidates, scores)

    score, awarded_seats = d[cats]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d[foxes]
    assert score == 13
    assert awarded_seats == -1

    candidates_to_add_to = [cats, foxes]
    scores = [5, 11]
    d.add_score(candidates_to_add_to, scores)

    score, awarded_seats = d[cats]
    assert score == 47
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 10 # bears should not change
    assert awarded_seats == -1

    score, awarded_seats = d[foxes]
    assert score == 24
    assert awarded_seats == -1


def test_set_to_multiple_candidates_list() -> None:
    """ Test that we can set the score of candidates using lists of parties and scores. """
    d = Distribution(1)

    candidates = [dogs, foxes, cats]
    scores = [42, 10, 13]

    d.add_score(candidates, scores)

    score, awarded_seats = d[dogs]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d[foxes]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d[cats]
    assert score == 13
    assert awarded_seats == -1

    candidates_to_set = [dogs, cats]
    scores = [5, 11]
    d.set_score(candidates_to_set, scores)

    score, awarded_seats = d[dogs]
    assert score == 5
    assert awarded_seats == -1

    score, awarded_seats = d[foxes]
    assert score == 10 # foxes should not change
    assert awarded_seats == -1

    score, awarded_seats = d[cats]
    assert score == 11
    assert awarded_seats == -1


def test_add_multiple_candidates_tuple() -> None:
    """ Test that we can add candidates by passing tuples of candidates and scores to the add_score method. """
    d = Distribution(1)

    candidates = (cats, dogs, bears)
    scores = (42, 10, 13)

    d.add_score(candidates, scores)

    score, awarded_seats = d[cats]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d[dogs]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 13
    assert awarded_seats == -1


def test_add_more_to_multiple_candidates_tuple() -> None:
    """ Test that we can add more score to candidates using tuples of parties and scores. """
    d = Distribution(1)

    candidates = (cats, foxes, bears)
    scores = (42, 10, 13)

    d.add_score(candidates, scores)

    score, awarded_seats = d[cats]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d[foxes]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 13
    assert awarded_seats == -1

    candidates_to_add_to = (cats, bears)
    scores = (5, 11)
    d.add_score(candidates_to_add_to, scores)

    score, awarded_seats = d[cats]
    assert score == 47
    assert awarded_seats == -1

    score, awarded_seats = d[foxes]
    assert score == 10 # foxes should not change
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 24
    assert awarded_seats == -1


def test_set_to_multiple_candidates_tuple() -> None:
    """ Test that we can set the score of candidates using tuples of IDs and scores. """
    d = Distribution(1)

    candidates = (dogs, bears, cats)
    scores = (42, 10, 13)

    d.add_score(candidates, scores)

    score, awarded_seats = d[dogs]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d[cats]
    assert score == 13
    assert awarded_seats == -1

    candidates_to_set = (dogs, cats)
    scores = (5, 11)
    d.set_score(candidates_to_set, scores)

    score, awarded_seats = d[dogs]
    assert score == 5
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 10 # bears should not change
    assert awarded_seats == -1

    score, awarded_seats = d[cats]
    assert score == 11
    assert awarded_seats == -1


def test_add_multiple_candidates_dict() -> None:
    """ Test that we can add candidates by passing a dictionary with candidates and scores to the add_score method. """
    d = Distribution(1)

    candidates = {
        cats: 42,
        dogs: 10,
        bears: 13
    }

    d.add_score(candidates)

    score, awarded_seats = d[cats]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d[dogs]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 13
    assert awarded_seats == -1


def test_add_more_to_multiple_candidates_dict() -> None:
    """ Test that we can add more score to candidates using a dictionary of parties and scores. """
    d = Distribution(1)

    candidates = {
        cats: 42,
        dogs: 10,
        bears: 13
    }

    d.add_score(candidates)

    score, awarded_seats = d[cats]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d[dogs]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 13
    assert awarded_seats == -1

    candidates_to_add_to = {
        cats: 5,
        bears: 11
    }
    d.add_score(candidates_to_add_to)

    score, awarded_seats = d[cats]
    assert score == 47
    assert awarded_seats == -1

    score, awarded_seats = d[dogs]
    assert score == 10 # dogs should not change
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 24
    assert awarded_seats == -1


def test_set_to_multiple_candidates_dict() -> None:
    """ Test that we can set the score of candidates using a dictionary of IDs and scores. """
    d = Distribution(1)

    candidates = {
        cats: 42,
        dogs: 10,
        bears: 13
    }

    d.add_score(candidates)

    score, awarded_seats = d[cats]
    assert score == 42
    assert awarded_seats == -1

    score, awarded_seats = d[dogs]
    assert score == 10
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 13
    assert awarded_seats == -1

    candidates_to_set = {
        cats: 5,
        bears: 11
    }
    d.set_score(candidates_to_set)

    score, awarded_seats = d[cats]
    assert score == 5
    assert awarded_seats == -1

    score, awarded_seats = d[dogs]
    assert score == 10 # dogs should not change
    assert awarded_seats == -1

    score, awarded_seats = d[bears]
    assert score == 11
    assert awarded_seats == -1


def test_CandidateDoesNotExistError() -> None:
    """ Test that we get a CandidateDoesNotExistError if trying to access the score of a candidate
    which does not exist, or if we try to remove a candidate which does not exist.
    """
    d = Distribution(1)
    d.add_score(cats, 10)

    with pytest.raises(CandidateDoesNotExistError):
        d.remove_candidate(bears)

    with pytest.raises(CandidateDoesNotExistError):
        score, awarded_seats = d[foxes]

    score, awarded_seats = d[cats]
    assert score == 10
    assert awarded_seats == -1


def test_remove_candidate() -> None:
    """ Test that we can add and remove a candidate without affecting other candidates. """
    d = Distribution(1)
    d.add_score([cats, foxes, dogs], [5, 7, 11])

    score, awarded_seats = d[cats]
    assert score == 5
    assert awarded_seats == -1

    score, awarded_seats = d[foxes]
    assert score == 7
    assert awarded_seats == -1

    score, awarded_seats = d[dogs]
    assert score == 11
    assert awarded_seats == -1

    d.remove_candidate(foxes)

    score, awarded_seats = d[cats]
    assert score == 5
    assert awarded_seats == -1

    with pytest.raises(CandidateDoesNotExistError):
        score, awarded_seats = d[foxes] # should get a CandidateDoesNotExistError on this now.

    score, awarded_seats = d[dogs]
    assert score == 11
    assert awarded_seats == -1

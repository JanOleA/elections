from multiprocessing.sharedctypes import Value
from typing import Any, Dict, Union

import numpy as np
import pandas as pd

from .utils import CandidateDoesNotExistError, Utils


class Distribution:
    def __init__(self, num_seats: int) -> None:
        """ Base class for various methods that distribute a given number of
        positions/seats etc. based one some score (votes, population, etc.).

        Add candidates with add_score(id, value) or set_score(id, value).
        Each candidate is identified with a string ID.

        Args:
            num_seats: Total number of seats available in the distribution.
        """
        self.num_seats = num_seats
        self._candidates: Dict[str, Union[int, float]] = {}
        self._result: Dict[str, int] = {}
        self._is_calculated = False
        self._true_ratios = None

    def add_scores_list(self,
                       candidate_ids_list: Union[list[str], tuple[str, ...]],
                       scores_list: Union[list[float], list[int], tuple[float, ...], tuple[int, ...]],
                       reset: bool = False) -> None:
        """ Add some scores to a given list/tuple of candidate IDs.
        
        Candidates that do not yet exist will be created.
        Args:
            candidate_ids_list: list/tuple containing the candidate IDs.
            scores_list: list/tuple containing matching scores for each candidate ID.

        Optional:
            reset: Resets the candidate score before adding it.
        """
        if len(candidate_ids_list) != len(scores_list):
            raise ValueError("Need matching number of candidate IDs and scores")
        for candidate_id, score in zip(candidate_ids_list, scores_list):
            self.add_score(candidate_id, score, reset = reset)

    def add_scores_dict(self, candidates_dict: Union[dict[str, int], dict[str, float]],
                        reset: bool = False) -> None:
        """ Add some scores to a given dictionary of candidate IDs.
        
        Candidates that do not yet exist will be created.
        Args:
            candidates_dict: dictionary with key/value pairs of IDs and scores to add.

        Optional:
            reset: Resets the candidate score before adding it.
        """
        for key, val in candidates_dict.items():
            self.add_score(key, val, reset = reset)

    def add_score(self,
                  candidate_id: Union[str, list[str], tuple[str, ...], dict[str, float], dict[str, int]],
                  score: Union[int, float, list[float], list[int], tuple[float, ...], tuple[int, ...], None] = None,
                  reset: bool=False) -> None:
        """ Add some score to the given candidate using its ID.
        
        If the candidate does not yet exist, it will be created.
        Multiple can be passed at the same time as two lists/tuples of ids/scores or as a single dictionary.

        Args:
            candidate_id: ID(s) for the candidate or dictionary with key/value pairs of IDs and scores.
            score(s): Value to add to the candidate.

        Optional:
            reset: Resets the candidate score before adding it.
        """
        if isinstance(candidate_id, dict):
            if score is None:
                self.add_scores_dict(candidate_id, reset = reset)
                return
            else:
                raise ValueError("If passing candidate ID as dictionary, score argument must be None.")
        elif Utils.is_list_or_tuple(candidate_id) and Utils.is_list_or_tuple(score):
            self.add_scores_list(candidate_id, score, reset = reset) # type: ignore (typing error from str, int and float not matching method input, but we are actually sure they are not str, int or float)
            return
        elif Utils.is_list_or_tuple(candidate_id): # candidate_id is list or tuple, but score is not
            raise ValueError("Can't pass list/tuple for candidate_id but not score.")
        elif Utils.is_list_or_tuple(score): # score is list or tuple, but candidate_id is not
            raise ValueError("Can't pass list/tuple for score but not candidate_id.")

        if not isinstance(candidate_id, str):
            raise ValueError(f"Incorrect type passed for candidate_id, expected string, got {type(candidate_id)}")
        if not (isinstance(score, int) or isinstance(score, float)):
            raise ValueError(f"Incorrect type passed for score, expected float or int, got {type(score)}")
        
        self._is_calculated = False # set _is_calculated to False, because the calculation must be redone if scores have changed
        self._true_ratios = None
        if reset: self._candidates[candidate_id] = 0
        if candidate_id in self._candidates:
            self._candidates[candidate_id] += score
        else:
            self._candidates[candidate_id] = score

    def set_score(self,
                  candidate_id: Union[str, list[str], tuple[str, ...], dict[str, float], dict[str, int]],
                  score: Union[int, float, list[float], list[int], tuple[float, ...], tuple[int, ...], None] = None) -> None:
        """ Set the score of some candidate using its ID.
        
        If the candidate does not yet exist, it will be created.
        Multiple can be passed at the same time as two lists/tuples of ids/scores.

        Args:
            candidate_id: ID for the candidate.
            score: Value to set for the candidate.
        """
        self.add_score(candidate_id, score, reset=True)

    def remove_candidate(self, candidate_id: str) -> None:
        """ Remove a candidate from the calculation.
        
        Raises a CandidateDoesNotExistError if the candidate is not added to the distribution.

        Args:
            candidate_id: ID for the candidate.
        """
        self._is_calculated = False # set _is_calculated to False because the calculation must be redone
        if candidate_id in self._candidates:
            del self._candidates[candidate_id]
        else:
            raise CandidateDoesNotExistError("Attempted to remove candidate which does not exist.")

    def calculate(self) -> None:
        raise NotImplementedError("Method must be implemented in a subclass.")

    def __getitem__(self, key: str) -> tuple[Union[float, int], int]:
        """ Return the score of a candidate and its number awarded seats if the calculation has been completed (otherwise -1).
        
        Raises a CandidateDoesNotExistError if the candidate is not yet added.

        Args:
            key: candidate ID

        Returns:
            A tuple with (score, awarded_seats)
        """
        if key in self._result and self._is_calculated:
            awarded_seats = self._result[key]
        else:
            awarded_seats = -1
        if key in self._candidates:
            return self._candidates[key], awarded_seats
        else:
            raise CandidateDoesNotExistError("Candidate has not been added to the distribution.")

    @property
    def result(self) -> dict[str, int]:
        if not self._is_calculated:
            self.calculate()
        return self._result.copy()

    @property
    def true_ratios(self) -> dict[str, float]:
        """ Returns the true ratio of seats a candidate should get given the total number of seats and its score. """
        if self._true_ratios is None:
            score_sum = sum(self._candidates.values())
            divisor = score_sum/self.num_seats
            self._true_ratios = {key: score/divisor for key, score in self._candidates.items()}
        return self._true_ratios

    @property
    def num_seats(self) -> int:
        return self._num_seats
    
    @num_seats.setter
    def num_seats(self, value: int) -> None:
        self._is_calculated = False
        self._true_ratios = None
        self._num_seats = value


class StLague(Distribution):
    def __init__(self,
                 num_seats: int,
                 initial_divisor: Union[float, int] = 1):
        """ Distribute seats according to the StLague method. 
        
        Args:
            initial_divisor: Set the initial divisor for the first seat. A higher value typically favors higher-scoring candidates.
        """
        super().__init__(num_seats)
        self.initial_divisor = initial_divisor

    def _new_divisor(self, awarded_seats: int) -> int:
        """ Calculate the divisor for a given number of awarded seats """
        return awarded_seats*2 + 1

    def calculate(self) -> Union[tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame], tuple[None, ...]]:
        """ Calculate the distribution.
        
        Returns:
            Three dataframes: score matrix, divisor matrix, awarded seats matrix
        """
        num_candidates = len(self._candidates)

        if num_candidates == 0:
            self._result = {}
            self._is_calculated = True
            return (None, None, None)

        awarded_seats = np.zeros(num_candidates, dtype = int)
        score_array = np.array(list(self._candidates.values())) # requires Python 3.7+ because the preservation of order in the dictionary is important
        divisor_array = np.full(num_candidates, self.initial_divisor)

        score_matrix = []
        divisor_matrix = []
        awarded_seats_matrix = []

        while np.sum(awarded_seats) < self.num_seats:
            new_scores = score_array/divisor_array
            next_seat_index = np.argmax(new_scores) # TODO: handle cases where multiple candidates have the same score
            divisor_matrix.append(divisor_array.copy())

            awarded_seats[next_seat_index] += 1
            divisor_array[next_seat_index] = self._new_divisor(awarded_seats[next_seat_index])

            score_matrix.append(new_scores.copy())
            awarded_seats_matrix.append(awarded_seats.copy())

        for candidate_id, seats in zip(self._candidates.keys(), awarded_seats):
            self._result[candidate_id] = seats
        
        score_df = pd.DataFrame(score_matrix)
        score_df.columns = list(self._candidates.keys())
        divisor_df = pd.DataFrame(divisor_matrix)
        divisor_df.columns = list(self._candidates.keys())
        awarded_seats_df = pd.DataFrame(awarded_seats_matrix)
        awarded_seats_df.columns = list(self._candidates.keys())

        self._is_calculated = True
        return score_df, divisor_df, awarded_seats_df

    @property
    def initial_divisor(self) -> Union[float, int]:
        return self._initial_divisor

    @initial_divisor.setter
    def initial_divisor(self, value: Union[float, int]) -> None:
        self._is_calculated = False
        self._initial_divisor = value


class DHondt(StLague):
    def __init__(self, num_seats: int, initial_divisor: Union[float, int] = 1):
        """ Distribute seats according to the DHondt method. 
        
        Args:
            initial_divisor: Set the initial divisor for the first seat. A higher value typically favors higher-scoring candidates.
        """
        super().__init__(num_seats, initial_divisor)

    def _new_divisor(self, awarded_seats: int) -> int:
        """ Calculate the divisor for a given number of awarded seats """
        return awarded_seats + 1


class FirstPastThePost(Distribution):
    def __init__(self, num_seats: int) -> None:
        """ Distribute seats according to the first past the post method (winner takes all). """
        super().__init__(num_seats)

    def calculate(self) -> None:
        """ Calculate the distribution. """
        if len(self._candidates) == 0:
            return

        # TODO: Handle multiple candidates with max score
        max_key = max(self._candidates, key=self._candidates.get) # type: ignore
        for key in self._candidates:
            if key == max_key:
                self._result[key] = self.num_seats
            else:
                self._result[key] = 0
        self._is_calculated = True
        

class HuntingtonHill(Distribution):
    def __init__(self,
                 num_seats: int,
                 initial_seats: int = 1,
                 threshold: float = 0) -> None:
        super().__init__(num_seats)
        self.initial_seats = initial_seats
        self.threshold = threshold

    def calculate(self) -> Union[tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame], tuple[None, ...]]:
        """ Calculate the distribution. """
        num_candidates = len(self._candidates)

        if num_candidates == 0:
            return None, None, None

        if num_candidates*self.initial_seats > self.num_seats:
            raise ValueError("Initial seats times number of candidates cannot be larger than the number of seats available.")

        sum_scores = sum(self._candidates.values())
        included_candidates_dict = {}
        for key, score in self._candidates.items():
            if score/sum_scores*100 >= self.threshold:
                included_candidates_dict[key] = score

        awarded_seats = np.full(num_candidates, self.initial_seats, dtype = int)
        score_array = np.array(list(self._candidates.values())) # requires Python 3.7+ because the preservation of order in the dictionary is important
        divisor_array = np.full(num_candidates, np.sqrt(self.initial_seats*(self.initial_seats + 1)))

        score_matrix = []
        divisor_matrix = []
        awarded_seats_matrix = []

        while np.sum(awarded_seats) < self.num_seats:
            new_scores = score_array/divisor_array
            next_seat_index = np.argmax(new_scores) # TODO: handle cases where multiple candidates have the same score
            divisor_matrix.append(divisor_array.copy())

            awarded_seats[next_seat_index] += 1
            awarded_seats_new = awarded_seats[next_seat_index]
            divisor_array[next_seat_index] = np.sqrt(awarded_seats_new*(awarded_seats_new + 1))

            score_matrix.append(new_scores.copy())
            awarded_seats_matrix.append(awarded_seats.copy())

        for candidate_id, seats in zip(self._candidates.keys(), awarded_seats):
            self._result[candidate_id] = seats
        
        score_df = pd.DataFrame(score_matrix)
        divisor_df = pd.DataFrame(divisor_matrix)
        awarded_seats_df = pd.DataFrame(awarded_seats_matrix)
        if len(score_matrix) > 0:
            score_df.columns = list(self._candidates.keys())
            divisor_df.columns = list(self._candidates.keys())
            awarded_seats_df.columns = list(self._candidates.keys())

        self._is_calculated = True
        return score_df, divisor_df, awarded_seats_df

    @property
    def initial_seats(self) -> int:
        return self._initial_seats

    @initial_seats.setter
    def initial_seats(self, value: int) -> None:
        self._is_calculated = False
        self._initial_seats = value

    @property
    def threshold(self) -> Union[int, float]:
        return self._threshold

    @threshold.setter
    def threshold(self, value: Union[int, float]) -> None:
        self._is_calculated = False
        self._threshold = value


class Hamilton(Distribution):
    def __init__(self, num_seats: int, quota: str = "hare") -> None:
        super().__init__(num_seats)
        if quota == "hare":
            self.quota = self._hare_quota
        elif quota == "droop":
            self.quota = self._droop_quota
        else:
            raise ValueError("Quota must one of: {'hare', 'droop'}")

    def _hare_quota(self) -> Union[int, float]:
        return sum(self._candidates.values()) / self.num_seats

    def _droop_quota(self) -> int:
        return int(1 + (sum(self._candidates.values()) / (1 + self.num_seats)))

    def calculate(self) -> Union[tuple[Any, Any], tuple[None, None]]:
        """ Calculate the distribution. """
        num_candidates = len(self._candidates)

        if num_candidates == 0:
            return None, None

        quota = self.quota()
        candidate_ids = list(self._candidates.keys())
        initial_scores = np.array(list(self._candidates.values()))/quota
        fractions, integer_scores = np.modf(initial_scores)
        frac_sort = np.argsort(fractions)[::-1]

        for key, score in zip(candidate_ids, integer_scores):
            self._result[key] = int(score)

        for index in frac_sort:
            if sum(self._result.values()) >= self.num_seats:
                break
            self._result[candidate_ids[index]] += 1

        self._is_calculated = True

        return integer_scores.astype(int), fractions


class Adams(Distribution):
    def __init__(self, num_seats: int) -> None:
        super().__init__(num_seats)

    def calculate(self) -> Union[float, None]:
        """ Calculate the distribution. """
        num_candidates = len(self._candidates)

        if num_candidates == 0:
            return

        divisor = sum(self._candidates.values())/self.num_seats # initial divisor
        step = divisor/100 # how much to step by to begin with

        candidate_ids = list(self._candidates.keys())
        candidate_scores = np.array(list(self._candidates.values()))
        awarded_seats = np.ceil(candidate_scores/divisor)

        while np.sum(awarded_seats) > self.num_seats:
            divisor += step
            awarded_seats = np.ceil(candidate_scores/divisor)
            if np.sum(awarded_seats) < self.num_seats: # if we overstepped, step back, recalculate and halve the step
                divisor -= step
                awarded_seats = np.ceil(candidate_scores/divisor)
                step /= 2

        for candidate_id, awards in zip(candidate_ids, awarded_seats):
            self._result[candidate_id] = int(awards)
        self._is_calculated = True

        return divisor # return the final divisor
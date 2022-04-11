from typing import Union


def hare(score_sum: Union[float, int], num_seats: int) -> float:
    return score_sum/num_seats


def droop(score_sum: Union[float, int], num_seats: int) -> float:
    return int(1 + (score_sum / (1 + num_seats)))


from typing import Any


class CandidateDoesNotExistError(Exception):
    """ To be raised in certain cases if the user attempts to use a candidate
    ID which is not added to the candidates.
    """


class Utils:
    @staticmethod
    def is_list_or_tuple(item: Any) -> bool:
        """ Check if an object is a list or a tuple """
        if isinstance(item, list) or isinstance(item, tuple):
            return True
        else:
            return False

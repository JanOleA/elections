from typing import Any, Union

from elections.party import Party
from .distribution.distribution import Distribution


class NotEnoughLevelingSeatsError(Exception):
    """ To be raised if a user tries to set more leveling seats in a district than there are available """


class _District:
    """ Base class for other district types """
    def __init__(self, name: str,
                 eligible_voters: Union[float, int],
                 area: Union[float, int],
                 location: Union[tuple[float, float], tuple[int, int]],
                 distribution: Union[Distribution, None]):
        """ Represents a physical location in elections where some of the calculation is done on a local level. """
        self.name = name
        self.location = location
        self.eligible_voters = eligible_voters
        self.area = area
        self.distribution = distribution
        self._result_details = None

    @property
    def eligible_voters(self) -> Union[int, float]:
        return self._eligible_voters
    
    @eligible_voters.setter
    def eligible_voters(self, value: Union[int, float]) -> None:
        self._eligible_voters = float(value)

    @property
    def area(self) -> Union[int, float]:
        return self._area
    
    @area.setter
    def area(self, value: Union[int, float]) -> None:
        self._area = float(value)

    @property
    def result(self) -> dict:
        if self.distribution is None:
            raise ValueError("Can't calculate a result because no distribution was defined for the district")
        self._result_details = self.distribution.calculate()
        return self.distribution.result

    @property
    def result_details(self) -> Any:
        return self._result_details

    @property
    def distribution(self) -> Union[Distribution, None]:
        return self._distribution

    @distribution.setter
    def distribution(self, dist: Union[Distribution, None]) -> None:
        if isinstance(dist, Distribution):
            self._distribution = dist
        elif dist is None:
            self._distribution = None
        else:
            raise ValueError(f"The distribution must be an instance of a subclass of Distribution, but was: {type(dist)}")

    def __repr__(self) -> str:
        return f"<{__name__}._District '{self.name}' at {hex(id(self))} with distribution: {self.distribution}>"

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = str(value)

    @property
    def location(self) -> Union[tuple[float, float], tuple[int, int]]:
        return self._location
    
    @location.setter
    def location(self, value: Union[tuple[float, float], tuple[int, int]]) -> None:
        self._location = value


class District(_District):
    def __init__(self, name: str,
                 eligible_voters: Union[float, int],
                 area: Union[float, int],
                 location: Union[tuple[float, float], tuple[int, int]] = (0, 0),
                 distribution: Union[Distribution, None] = None):
        super().__init__(name, eligible_voters, area, location, distribution)

    def __repr__(self) -> str:
        return f"<{__name__}.District '{self.name}' at {hex(id(self))} with distribution: {self.distribution}>"

class NorwegianFylke(District):
    def __init__(self, fylkeid: int,
                 eligible_voters: Union[float, int],
                 area: Union[float, int],
                 location: Union[tuple[float, float], tuple[int, int]] = (0, 0),
                 distribution: Union[Distribution, None] = None,
                 name: str = ""):
        """ Specific district type for Norwegian elections, with support for leveling seats """
        if not name: name = str(fylkeid)
        super().__init__(name, eligible_voters, area, location, distribution)
        self.fylkeid = fylkeid
        self.available_leveling_seats = 1
        self._leveling_seats: list[Union[str, Party]] = [] # list for holding the winners of leveling seats

    def add_leveling_seat_winner(self, candidate: Union[str, Party]) -> None:
        if len(self.leveling_seats) < self.available_leveling_seats:
            self._leveling_seats.append(candidate)
        else:
            raise NotEnoughLevelingSeatsError(f"Can't add more leveling seat winners to this district (max={self.available_leveling_seats})")

    def remove_leveling_seat_winner(self, candidate: Union[str, Party]) -> None:
        self._leveling_seats.remove(candidate)

    def clear_leveling_seat_winners(self) -> None:
        self._leveling_seats = []

    @property
    def fylkeid(self) -> int:
        return self._fylkeid
    
    @fylkeid.setter
    def fylkeid(self, value: int) -> None:
        self._fylkeid = int(value)

    @property
    def leveling_seats(self) -> list[Union[str, Party]]:
        return self._leveling_seats

    @property
    def available_leveling_seats(self) -> int:
        return self._available_leveling_seats
    
    @available_leveling_seats.setter
    def available_leveling_seats(self, value: int) -> None:
        self._available_leveling_seats = int(value)

    def __repr__(self) -> str:
        return f"<{__name__}.NorwegianFylke '{self.name}' at {hex(id(self))} with distribution: {self.distribution}, available_leveling_seats={self.available_leveling_seats}>"
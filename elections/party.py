from typing import Union

class Party:
    def __init__(self, name: str,
                 spectrum_position: float = 0,
                 color: str = "#888",
                 total_votes: Union[int, float] = 0,
                 seats_awarded: int = 0) -> None:
        self.name = name
        self.spectrum_position = spectrum_position
        self.color = color
        self.total_votes = total_votes
        self.seats_awarded = seats_awarded

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = str(value)

    @property
    def spectrum_position(self) -> float:
        return self._spectrum_position

    @spectrum_position.setter
    def spectrum_position(self, value: float) -> None:
        self._spectrum_position = float(value)

    @property
    def color(self) -> str:
        return self._color
    
    @color.setter
    def color(self, value: str) -> None:
        self._color = str(value)

    @property
    def total_votes(self) -> Union[int, float]:
        return self._total_votes
    
    @total_votes.setter
    def total_votes(self, value: Union[int, float]) -> None:
        self._total_votes = float(value)

    @property
    def seats_awarded(self) -> int:
        return self._seats_awarded
    
    @seats_awarded.setter
    def seats_awarded(self, value: int) -> None:
        self._seats_awarded = int(value)

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"<{__name__}.Party, name={self.name}, spectrum_position={self.spectrum_position}, color={self.color} at {hex(id(self))}>"
# elections
Python package with functionality for simple election result calculation and analysis

## Current apportionment methods implemented:
- StLague
- DHondt
- FirstPastThePost
- HuntingtonHill
- Hamilton
- Adams

## Party class
Define parties with a custom Party type, giving them a name, position on the political spectrum, color, etc. Can be used seamlessly with the apportionment classes.

## National district class
For elections where results are calculated in local districts, there are several types of district types included.

All district types have support for location (so they can be plotted on a map), individual apportionment in the district, and more.

- Generic district
- Norwegian fylke
    - Functionality for easy calculation of leveling seat distribution in national elections

## Examples:
### Easy and fast to calculate results:
```python
from pylections import distributions

populations = {
    "New Triangle": 21878,
    "Circula": 9713,
    "Squaryland": 4167,
    "Octiana": 3252,
    "Rhombus Island": 1065
}

hamilton = distributions.Hamilton.get(num_seats=43, candidates=populations)
for name, seats in hamilton.items():
    print(name, seats)

"""
New Triangle 24
Circula 10
Squaryland 4
Octiana 4
Rhombus Island 1
"""

hamilton = distributions.Hamilton.get(num_seats=43, candidates=populations, quota="droop")
for name, seats in hamilton.items():
    print(name, seats)

"""
New Triangle 24
Circula 11
Squaryland 4
Octiana 3
Rhombus Island 1
"""

adams = distributions.Adams.get(num_seats=43, candidates=populations)
for name, seats in adams.items():
    print(name, seats)

"""
New Triangle 22
Circula 10
Squaryland 5
Octiana 4
Rhombus Island 2
"""
```

### Flexible with OOP:
```python
populations = {
    "New Triangle": 21878,
    "Circula": 9713,
    "Squaryland": 4167,
    "Octiana": 3252,
    "Rhombus Island": 1065
}

stlague = distributions.StLague(num_seats = 43)
stlague.add_score(populations)

for name, seats in stlague.result.items():
    print(name, seats)

"""
New Triangle 24
Circula 10
Squaryland 4
Octiana 4
Rhombus Island 1
"""

stlague.num_seats = 44
for name, seats in stlague.result.items():
    print(name, seats)

"""
New Triangle 24
Circula 10
Squaryland 5
Octiana 4
Rhombus Island 1
"""

stlague.remove_candidate("New Triangle")
for name, seats in stlague.result.items():
    print(name, seats)

"""
Circula 23
Squaryland 10
Octiana 8
Rhombus Island 3
"""

stlague.add_score("Rhombus Island", 1623)
for name, seats in stlague.result.items():
    print(name, seats)

"""
Circula 22
Squaryland 9
Octiana 7
Rhombus Island 6
"""
```

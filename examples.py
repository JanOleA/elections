from pylections import distributions

populations = {
    "New Triangle": 21878,
    "Circula": 9713,
    "Squaryland": 4167,
    "Octiana": 3252,
    "Rhombus Island": 1065
}

print("Hamilton, hare quota")
hamilton = distributions.Hamilton.get(num_seats=43, candidates=populations)
for name, seats in hamilton.items():
    print(name, seats)

print("\nHamilton, droop quota")
hamilton = distributions.Hamilton.get(num_seats=43, candidates=populations, quota="droop")
for name, seats in hamilton.items():
    print(name, seats)

print("\nAdams")
adams = distributions.Adams.get(num_seats=43, candidates=populations)
for name, seats in adams.items():
    print(name, seats)

stlague = distributions.StLague(num_seats=43)
stlague.add_score(populations)

print("\nStLague, 43 seats")
for name, seats in stlague.result.items():
    print(name, seats)

print("\nStLague, 44 seats")
stlague.num_seats = 44
for name, seats in stlague.result.items():
    print(name, seats)

print("\nStLague, New Triangle removed")
stlague.remove_candidate("New Triangle")
for name, seats in stlague.result.items():
    print(name, seats)

print("\nStLague, Add score to Rhombus Island")
stlague.add_score("Rhombus Island", 1623)
for name, seats in stlague.result.items():
    print(name, seats)
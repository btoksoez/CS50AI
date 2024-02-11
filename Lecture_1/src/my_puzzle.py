from logic import *

people = ["Gilderoy", "Pomona", "Minerva", "Horace"]
houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

symbols = []

for person in people:
    for house in houses:
        symbols.append(And(Symbol(person), Symbol(house)))

def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            print(f"{symbol}: YES")
        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: MAYBE")
        elif model_check(knowledge, Not(symbol)):
            print(f"{symbol}: NO")

combinations = []
combis = []
knowledge = And()

# Generate all possible combinations of people and houses
i = 0
while i in range(len(people)):
    j = 0
    for j in range(len(houses)):
        person = people[i]
        house = houses[j]
        combinations.append(And(Symbol(person), Symbol(house)))
        j += 1
    combis.append(And(*combinations))
    i += 1


# Create an Or statement to combine all combinations
knowledge.add(Or(*combinations))

knowledge.add(Or(And(Symbol(f"Gilderoy"), Symbol("Ravenclaw")), And(Symbol(f"Gilderoy"), Symbol("Gryffindor"))))
knowledge.add(Not(And(Symbol("Pomona"), Symbol("Slytherin"))))
knowledge.add(And(Symbol("Minerva"), Symbol("Gryffindor")))

print(knowledge.formula)
check_knowledge(knowledge)





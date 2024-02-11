from logic import *

colors = ["red", "blue", "green", "yellow"]
symbols = []
for i in range(4):
    for color in colors:
        symbols.append(Symbol(f"{color}{i}"))

knowledge = And()
# Each color has one position
for color in colors:
    knowledge.add(
        Or(Symbol(f"{color}{1}"),
           Symbol(f"{color}{2}"),
           Symbol(f"{color}{3}"),
           Symbol(f"{color}{4}"),
        )
)

# Only one color per position
for position in range(4):
    for c1 in colors:
        for c2 in colors:
            if c1 != c2:
                knowledge.add(Implication((Symbol(f"{c1}{position}")), Not(Symbol(f"{c2}{position}"))))

# Only one position per color.
for color in colors:
    for i in range(4):
        for j in range(4):
            if i != j:
                knowledge.add(Implication(
                    Symbol(f"{color}{i}"), Not(Symbol(f"{color}{j}"))
                ))

#Correct position meaning
                

print(knowledge.formula)
def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            print(f"{symbol}: YES")
        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: MAYBE")
        elif model_check(knowledge, Not(symbol)):
            print(f"{symbol}: NO")



print(check_knowledge(knowledge))
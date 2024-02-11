from logic import *

# define symbols
mustard = Symbol("mustard")
plum = Symbol("plum")
...

knowledge = And(
	Or(mustard, plum),
	Not(plum)
)

print(model_check(knowledge, mustard))


import nim_ai1
import nim
from collections import Counter

ai1 = nim.train(10000)
ai2 = nim_ai1.train(10000)



winners = []
n_games = 100000
for _ in range (n_games):
	winners.append(nim_ai1.play(ai1, ai2))

ai_counts = Counter(winners)

print(f'Count of ai1: {float(ai_counts["AI1"] * 100 / n_games)}')
print(f'Count of ai2: {float(ai_counts["AI2"] * 100 / n_games)}')



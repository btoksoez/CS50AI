from minesweeper import *

s1 = Sentence(cells={'A1', 'B2', 'C3'}, count=3)
s2 = Sentence(cells={'A1', 'B3', 'C1'}, count=3)
s3 = Sentence(cells={'A2', 'B5', 'C2'}, count=3)
sentences = [s1, s2, s3]
for sentence in sentences:
    print(f"Sentence: {sentence}\n")
    mines = sentence.known_mines()
    for mine in mines:
        print(f"Mine: {mine}\n")
    safes = sentence.known_safes()
    for safe in safes:
        print(f"Safe: {safe}\n")

s1.mark_safe('A1')

print("\n")
for sentence in sentences:
    print(f"Sentence: {sentence}\n")
    mines = sentence.known_mines()
    for mine in mines:
        print(f"Mine: {mine}\n")
    safes = sentence.known_safes()
    for safe in safes:
        print(f"Safe: {safe}\n")


ai = MinesweeperAI()
print(ai.make_safe_move())
print(ai.make_random_move())


from minesweeper import *

s = Sentence(cells={'A1', 'B2', 'C3'}, count=3)
print(Sentence.known_mines)
print(s)

def test_add_knowledge():
    ai = MinesweeperAI()

    # Add some initial knowledge
    ai.add_knowledge((0, 0), 1)
    ai.add_knowledge((1, 1), 2)
    ai.add_knowledge((2, 2), 0)

    # Check if initial knowledge has been added correctly
    assert len(ai.knowledge) == 3

    # Add some more knowledge
    ai.add_knowledge((0, 1), 0)
    ai.add_knowledge((1, 2), 1)

    # Check if new knowledge has been added correctly
    assert len(ai.knowledge) == 5

    # Add redundant knowledge
    ai.add_knowledge((0, 0), 1)
    ai.add_knowledge((1, 1), 2)

    # Check if redundant knowledge has been ignored
    assert len(ai.knowledge) == 5

    print("All tests passed!")

# Run the test
test_add_knowledge()

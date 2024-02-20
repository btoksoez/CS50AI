import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count != 0:
            return self.cells.copy()
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells.copy()
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) add cell to moves
        self.moves_made.add(cell)
        print(f"Cell: {cell}\n")

        # 2) mark cell as safe
        self.mark_safe(cell)

        # 3) add new cells as sentence
        new_cells = set()

        #   Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Ignore cells that are known already
                if (i, j) in self.safes:
                    continue
                if (i, j) in self.mines:
                    count = count - 1
                    continue

                # Add cells to new_cells
                if 0 <= i < self.height and 0 <= j < self.width:
                    new_cells.add((i, j))
                    print(f"new cell added: {i, j}\n")

        #   Add new sentence
        new_sentence = Sentence(new_cells, count)
        print(f"New Sentence: {new_sentence}\n")

        #   check sentence
        if new_sentence.count < 0 or new_sentence.cells == set():
            return

        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        #   Add safe cells
        if new_sentence.count == 0:
            for cell in new_cells:
                self.mark_safe(cell)

        #   Add mines
        if new_sentence.count == len(new_cells):
            for cell in new_cells:
                self.mark_mine(cell)

        # 4) Infer new knowledge
        knowledge_changed = True

        while(knowledge_changed):
            knowledge_changed = False

            safes = set()
            mines = set()

            for sentence in self.knowledge:
                if sentence.count == 0:
                    for cell in new_cells:
                        self.mark_safe(cell)

                if sentence.count == len(new_cells):
                    for cell in new_cells:
                        self.mark_mine(cell)

            safes.union(sentence.known_safes())
            mines.union(sentence.known_mines())


            if safes:
                knowledge_changed = True
                for safe in safes:
                    self.mark_safe(safe)

            if mines:
                knowledge_changed = True
                for mine in mines:
                    self.mark_mine(mine)

            # Remove empty sentences from KB
            empty_sentence = Sentence(set(), 0)

            self.knowledge[:] = [sentence for sentence in self.knowledge if sentence != empty_sentence]

        # 5) infer subsets
            for sentence_1 in self.knowledge:
                for sentence_2 in self.knowledge:
                    if sentence_1.cells == sentence_2.cells:
                        continue
                    if sentence_1.cells == set() and sentence_1.count > 0:
                        print('Error - sentence with no cells and count created')
                        raise ValueError
                    if sentence_1.cells.issubset(sentence_2.cells):
                        inferred_sentence = Sentence((sentence_2.cells - sentence_1.cells), (sentence_2.count - sentence_1.count))
                        if inferred_sentence not in self.knowledge:
                            knowledge_changed = True
                            print('New Inferred Knowledge: ', inferred_sentence, 'from', sentence_1, ' and ', sentence_2)
                            self.knowledge.append(inferred_sentence)

        print('Current AI KB length: ', len(self.knowledge))
        print('Known Mines: ', self.mines)
        print('Known Safes: ', self.safes)
        print('Safe Moves Remaining: ', self.safes - self.moves_made)
        print('====================================================')


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.all_cells():
            if cell in self.safes and cell not in self.moves_made:
                return (cell)
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        available_cells = self.all_cells() - self.mines - self.moves_made
        if available_cells:
            return random.choice(list(available_cells))
        else:
            return None


    def all_cells(self):
        cells = set()
        for i in range(self.height):
            for j in range(self.width):
                    cells.add((i, j))
        return cells


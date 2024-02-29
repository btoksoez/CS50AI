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
        # If the number of cells is equal to the count and not 0,
        # then all of that sentence's cells must be mines
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If we have sentence whose count is 0, we know that
        # all sentence's cells must be safe
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            # If we know that cell is a mine, then we decrease count of mines
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            # When cell is safe then we just remove it from sentence
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
            # For each sentence in self.knowledge, it calls the
            # mark_mine method(!) of the sentence object, passing
            # the cell as an argument.

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            # (mark_safe() is a method from its object!)

    def update_safe_and_mines(self):
        """
        updates safes and mines in internal knowledge based
        on sentences in KB
        """
        for sentence in self.knowledge:
            sentence_mines = sentence.known_mines()
            if sentence_mines:
                # We have to use copy of set to not alter its content
                # during checking operation to avoid possibility of infinite loop
                for cell in sentence_mines.copy():
                    self.mark_mine(cell)

            # And similar for safes
            sentence_safes = sentence.known_safes()
            if sentence_safes:
                for cell in sentence_safes.copy():
                    self.mark_safe(cell)

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
        # 1. Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2. Mark the cell as safe
        self.mark_safe(cell)

        # 3. Add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`

        # Find neighbors of cell to create a sentence. Loop over all cells
        # within one row and column and check if neighbor is in bounds and is unconfirmed
        new_cells = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # If cell is a known mine then decrease mines count and continue
                if (i, j) in self.mines:
                    count -= 1
                    continue

                # If we know that the cell is already safe then continue loop
                if (i, j) in self.safes:
                    continue

                # After all can be an unconfirmed neighbor if cell is in grid's bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    new_cells.add((i, j))

        # Creating sentence object with all unconfirmed neighbors and
        # number of mines around the cell minus number of known mines (already flagged)
        new_sentence = Sentence(new_cells, count)

        # Add a new sentence to the knowledge base:
        self.knowledge.append(new_sentence)

        # 4. Mark any additional cells as safe or as mines if it
        # can be concluded based on the AI's knowledge base

        self.update_safe_and_mines()

        # Remove empty sentence objects from list using list comprehension
        empty_sentence = Sentence(set(), 0)
        self.knowledge = [sentence for sentence in self.knowledge if sentence != empty_sentence]

        # 5. Add any new sentences to the AI's Knowledge Base
        # if they can be inferred from existing knowledge

        # Looking for the subsets of sets
        # Number of sentences in knowledge list

        for sentence_subset in self.knowledge:
            # Looping through sentences - looking for possible subset
            for sentence_superset in self.knowledge:
                # Looping through possible superset
                # Avoiding checking subset of itself (same memory location)
                if sentence_subset is sentence_superset:
                    continue

                # Get rid of duplicates (same content)
                if sentence_subset == sentence_superset:
                    self.knowledge.remove(sentence_superset)

                # If found subset
                if sentence_subset.cells.issubset(sentence_superset.cells):
                    # Remove the same cells from superset
                    result_set = sentence_superset.cells - sentence_subset.cells
                    # Subtract amount of mines
                    result_count = sentence_superset.count - sentence_subset.count
                    # Create new sentence
                    new_knowledge = Sentence(result_set, result_count)
                    # And add to the knowledge list only when it is new knowledge
                    if new_knowledge not in self.knowledge:
                        self.knowledge.append(new_knowledge)
        self.update_safe_and_mines()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Loop through safe cells
        for safe_cell in self.safes:
            # Check if we were already in this cell
            if safe_cell not in self.moves_made:
                return safe_cell
        # If there it is not possible to make safe move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_cells = []
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                # Search for any cell which is not a mine and was not visited yet
                if cell not in self.moves_made and cell not in self.mines:
                    possible_cells.append(cell)

        if len(possible_cells) == 0:
            # If not found any cell which is not a mine and not visited cell
            return None
        else:
            # Return a random cell chosen from possible moves
            return random.choice(possible_cells)

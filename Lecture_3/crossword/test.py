from generate import *
from crossword import *

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)

    print(creator.domains)
    creator.solve()
    print('\n')
    print(creator.domains)
    for x in creator.domains.copy():
        for y in creator.domains.copy():
            print(crossword.overlaps.get(x))
            creator.revise(x, y)
    print('\n')
    for x, words in creator.domains.items():
        print(x, words)

    print("\n")
    print(crossword.overlaps)





if __name__ == "__main__":
    main()

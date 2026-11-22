import random

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
vowels = ['a', 'e', 'i', 'o', 'u']


def create_grid(alphabet, vowels):
    lettermix = []
    for i in range(5):
        lettermix.append(random.choice(vowels))
    for i in range(11):
        lettermix.append(random.choice(alphabet))
    print(lettermix)

    grid = [[], [], [], []]
    for i in range(4):
        for j in range(4):
            letter = random.choice(lettermix)
            grid[i].append(letter)
            lettermix.remove(letter)
    return grid

# COME BACK TO THIS - NICER DISPLAY


def display_grid(grid):
    print(" \nSquardle\n ")
    for i in range(len(grid)):
        print(grid[i])


def end_game():
    print("ending...")
    return True


def display_rules():
    print(" \nRULES:\n- Words must be >= four letters\n- Letters must neighbour horizontally vertically or diagonally.\n- Each letter in a position on the grid can only be used once per word.\n ")


def check_word(Option, gridwords, remaining):
    Option = Option.upper()
    if len(Option) <= 3:
        return (" \nWords must be four letters or longer"), False
    elif Option not in gridwords:
        return (" \nInvalid word\n "), False
    elif Option in remaining:
        remaining.remove(Option)
        if len(remaining) == 0:
            return (" \nWell Done! You finished the Squardle!"), True
        return (" \nWell Done! You have " + str(len(remaining)) + " words left!"), False
    else:
        return (" \nYou already found that word."), False


def display_menu(End, grid, gridwords, remaining):
    display_grid(grid)
    Option = input(
        " \n- R to see rules\n- E to end the game\nOr enter your word:\n")
    if Option.upper() == 'R':
        display_rules()
    elif Option.upper() == 'E':
        print("You found "+str(len(gridwords)-len(remaining)) +
              " words out of "+str(len(gridwords))+"!")
        End = True
    else:
        Result, completed = check_word(Option, gridwords, remaining)
        print(Result)
        if completed:
            End = True
    return End


#  ƒinding all possible words


def find_words(grid, validwords):

    words = set()
    for word in validwords:
        if 16 >= len(word) >= 4:
            words.add(word)

    found = set()
    used = set()

    def search_grid(row, col, path):
        position = (row, col)
        # stops you from going to the current position or an earlier one as the next position in the path
        if position in used:
            return

        path = path + grid[row][col].upper()

        if len(path) >= 4 and path in words:
            found.add(path)
        used.add(position)

        # sets the range to the row/column before and after, unless its on the edge of the grid in which case it will be 0 or 4)
        for next_row in range(max(0, row - 1), min(4, row + 2)):
            for next_col in range(max(0, col - 1), min(4, col + 2)):
                search_grid(next_row, next_col, path)

        used.remove(position)

    for row in range(4):
        for column in range(4):
            search_grid(row, column, "")
    return found


# main
validwords = []
with open("CSW21.txt", 'r') as Wordlist:
    for line in Wordlist:
        words = line.split()
        if words and not words[0].startswith("#"):
            validwords.append(words[0])
print(validwords[0:10])


grid = create_grid(alphabet, vowels)

# display_rules()


gridwords = find_words(grid, validwords)
print(gridwords)
remaining = set(gridwords)

End = False
while not End:
    End = display_menu(End, grid, gridwords, remaining)

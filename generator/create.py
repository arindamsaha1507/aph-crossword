"""Creates the grid"""

from dataclasses import dataclass, field

import os
import random

WORDS = [
    "Sachin",
    "Biryani",
    "Simba",
    "HP",
    "Star Wars",
    "Kipling",
    "Spotify",
    "Scrolling",
    "Santa",
    "Kindle",
    "Messi",
    "Swift",
    "Lakshya",
    "Aurora",
    "Blackberry",
]


@dataclass
class Position:
    """Position on the grid"""

    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@dataclass
class Word:
    """Word class"""

    word: str
    intersection_points: list[int] = field(init=False, default_factory=list)
    position: Position = field(init=False)
    direction: bool = field(init=False)

    def __post_init__(self):
        self.capitalize()
        self.remove_spaces()
        self.position = Position(-1, -1)
        self.direction = True

    @property
    def length(self) -> int:
        """Returns the length of the word"""

        return len(self.word)

    @property
    def letter_indices(self) -> dict[str, int]:
        """Returns the letter indices of the word"""

        letter_dict = {}

        for index, letter in enumerate(self.word):
            if letter in letter_dict:
                letter_dict[letter].append(index)
            else:
                letter_dict[letter] = [index]

        return letter_dict

    def capitalize(self):
        """Capitalizes the word"""

        self.word = self.word.upper()

    def remove_spaces(self):
        """Removes spaces from the word"""

        self.word = self.word.replace(" ", "")

    def __hash__(self):
        return hash(self.word)

    def __eq__(self, other):
        return self.word == other.word

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.word


@dataclass
class Cell:
    """Cell class"""

    position: Position
    letter: str
    words: list[Word] = field(init=False, default_factory=list)

    def add_word(self, word: Word):
        """Adds a word to the cell"""

        if len(self.words) == 2:
            raise ValueError("Cell already has two words")

        self.words.append(word)

    def is_word_in_cell(self, word: Word) -> bool:
        """Returns whether the word is in the cell"""

        return word in self.words

    def is_intersection(self) -> bool:
        """Returns whether the cell is an intersection"""

        return len(self.words) == 2


@dataclass
class Grid:
    """Grid class"""

    grid: list[Cell] = field(init=False, default_factory=list)

    def normalize(self):
        """Normalizes the grid"""

        x_min = min(cell.position.x for cell in self.grid)
        y_min = min(cell.position.y for cell in self.grid)

        for cell in self.grid:
            cell.position.x -= x_min
            cell.position.y -= y_min

    def draw(self, filename: str = None):
        """Draws the grid"""

        self.normalize()

        x_max = max(cell.position.x for cell in self.grid)
        y_max = max(cell.position.y for cell in self.grid)

        with open(filename, "a") as file:

            for y in range(y_max + 1):
                for x in range(x_max + 1):
                    cell = next(
                        (
                            cell
                            for cell in self.grid
                            if cell.position.x == x and cell.position.y == y
                        ),
                        None,
                    )

                    if cell:
                        file.write(cell.letter)
                        file.write(" ")
                    else:
                        file.write("  ")

                file.write("\n")

            file.write("\n")
            file.write("=====================================")
            file.write("\n")

    def add_first_word(self, word: Word):
        """Adds the first word to the grid"""

        word.position = Position(0, 0)
        word.direction = True

        for index, letter in enumerate(word.word):
            position = Position(index, 0)
            cell = Cell(position, letter)
            cell.add_word(word)
            self.grid.append(cell)

    def get_intersection_points(self, word: Word) -> list[tuple[Position, int]]:
        """Returns the intersection points of the word"""

        print(f"Getting intersection points for {word}")
        print("Grid:")

        # for cell in self.grid:
        #     print(cell.position, cell.letter)

        intersection_points = []

        for cell in self.grid:

            # print(cell.position, cell.letter)
            # print(intersection_points)

            if cell.is_intersection():
                print("Cell is intersection")
                continue

            if cell.letter in word.word:
                print("Letter found in word")
                letter_indices = word.letter_indices[cell.letter]
                print("Letter indices", letter_indices)

                for index in letter_indices:
                    # if cell.position.x == index:
                    intersection_points.append((cell.position, index))

        print("Intersection points", intersection_points)
        return intersection_points

    def add_to_grid(
        self, word: Word, intersection_point: tuple[Position, int]
    ) -> list[Cell]:
        """Adds the word to the grid"""

        intersection_position = intersection_point[0]
        intersetion_letter_index = intersection_point[1]

        new_grid = self.grid.copy()

        intersection_cell = next(
            (cell for cell in new_grid if cell.position == intersection_position),
            None,
        )

        if not intersection_cell:
            raise ValueError("Intersection cell not found")

        existing_word_direction = intersection_cell.words[0].direction
        new_word_direction = not existing_word_direction
        word.direction = new_word_direction

        string = f"Trying to add {word.word} to {intersection_cell.words[0].word} at {intersection_position} with direction {new_word_direction}"
        print(string)

        for index, letter in enumerate(word.word):

            if new_word_direction:
                position = Position(
                    intersection_position.x - intersetion_letter_index + index,
                    intersection_position.y,
                )

            else:
                position = Position(
                    intersection_position.x,
                    intersection_position.y - intersetion_letter_index + index,
                )

            neighbor_positions = [
                Position(position.x, position.y - 1),
                Position(position.x, position.y + 1),
                Position(position.x - 1, position.y),
                Position(position.x + 1, position.y),
            ]

            neighbor_cells = [
                cell for cell in new_grid if cell.position in neighbor_positions
            ]

            for neighbor_cell in neighbor_cells:

                print(
                    "Neighbor cell",
                    neighbor_cell.position,
                    neighbor_cell.letter,
                    neighbor_cell.words[0].direction,
                )
                print("New word direction", new_word_direction)

                if (
                    neighbor_cell.words[0].direction == new_word_direction
                    and not neighbor_cell.is_intersection()
                    and not neighbor_cell.is_word_in_cell(word)
                ):
                    print(
                        f"Conflict while adding {word} at {position}. The neighbor cell {neighbor_cell.position} has the same direction"
                    )
                    return

            existing_cell = next(
                (cell for cell in new_grid if cell.position == position),
                None,
            )

            if existing_cell:
                if existing_cell.letter != letter:
                    print(
                        f"Conflict while adding {word} at {position}. The existing letter is {existing_cell.letter} and the new letter is {letter}"
                    )
                    return

                existing_cell.add_word(word)

            else:
                new_cell = Cell(position, letter)
                new_cell.add_word(word)
                new_grid.append(new_cell)

        return new_grid

    def add_word(self, word: Word):
        """Adds a word to the grid"""

        if len(self.grid) == 0:
            self.add_first_word(word)
            return

        intersection_points = self.get_intersection_points(word)

        if not intersection_points:
            print(f"Word {word} has no intersection points")
            return

        random.shuffle(intersection_points)

        for intersection_point in intersection_points:
            new_grid = self.add_to_grid(word, intersection_point)

            if new_grid:
                self.grid = new_grid
                return

        raise ValueError(f"Could not add word {word} due to conflicts")

    @property
    def dimensions(self) -> tuple[int, int]:
        """Returns the dimensions of the grid"""

        self.normalize()

        x_max = max(cell.position.x for cell in self.grid)
        y_max = max(cell.position.y for cell in self.grid)

        return (x_max + 1, y_max + 1)


def main():
    """Main function"""

    grid = Grid()

    words = [Word(word) for word in WORDS]
    random.shuffle(words)

    for word in words:
        grid.add_word(word)
        print("Added", word)
        grid.draw(filename="grid.txt")

    number_of_words = len(words)
    words_added = set(word for cell in grid.grid for word in cell.words)
    number_of_words_added = len(words_added)

    return {
        "grid": grid,
        "number_of_words": number_of_words,
        "number_of_words_added": number_of_words_added,
        "shape": grid.dimensions,
    }


if __name__ == "__main__":

    os.remove("grid.txt")

    resutls = []

    for _ in range(100):

        try:
            grid = main()
            resutls.append(grid)

        except ValueError as error:
            print(error)
            continue

    if os.path.exists("results.txt"):
        os.remove("results.txt")

    with open("results.txt", "w", encoding="utf-8") as file:
        for grid in resutls:
            file.write(f"Number of words: {grid['number_of_words']}\n")
            file.write(f"Number of words added: {grid['number_of_words_added']}\n")
            file.write(f"Shape: {grid['shape']}\n")
            file.write("\n")
            # grid["grid"].draw(filename="results.txt")

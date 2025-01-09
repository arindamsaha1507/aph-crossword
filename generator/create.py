"""Creates the grid"""

from dataclasses import dataclass, field

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
    direction: str = field(init=False)

    def __post_init__(self):
        self.capitalize()
        self.remove_spaces()
        self.position = Position(-1, -1)
        self.direction = "D"

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
class Tree:
    """Tree class"""

    words: list[Word]
    links: dict[tuple[Word, Word], tuple[int, int]] = field(
        init=False, default_factory=dict
    )
    tree: dict[tuple[Word, Word], tuple[int, int]] = field(
        init=False, default_factory=dict
    )

    def __post_init__(self):
        self.create_links()
        self.create_tree()

    def create_tree(self):
        """Creates the tree"""

        self.tree = {}

        links_copy = self.links.copy()

        while not self.check_if_tree_complete() and links_copy:

            link = random.choice(list(links_copy.keys()))
            intersection = links_copy[link]
            self.tree[link] = intersection
            del links_copy[link]

    def check_if_tree_complete(self) -> bool:
        """Checks if the tree is complete"""

        pairs = self.tree.keys()
        tree_words = [pair[0] for pair in pairs] + [pair[1] for pair in pairs]
        tree_words_set = set(tree_words)
        given_word_set = set(self.words)

        return tree_words_set == given_word_set

    def create_links(self):
        """Creates the links between the words"""

        word_index1 = 0
        word_index2 = word_index1 + 1

        while word_index2 < len(self.words):
            word1 = self.words[word_index1]
            word2 = self.words[word_index2]

            intersection = self.find_intersection(word1, word2)

            if intersection != (-1, -1):
                self.links[(word1, word2)] = intersection

            word_index2 += 1

            if word_index2 == len(self.words):
                word_index1 += 1
                word_index2 = word_index1 + 1

    def find_intersection(self, word1: Word, word2: Word) -> tuple[int, int]:
        """Finds the intersection between two words"""

        common_letters = []
        for letter in word1.letter_indices:
            if letter in word2.letter_indices:
                common_letters.append(letter)

        if not common_letters:
            return (-1, -1)

        for letter in common_letters:

            indices1 = word1.letter_indices[letter]
            indices2 = word2.letter_indices[letter]

            intersection1 = -1
            intersection2 = -1

            for index1 in indices1:
                if index1 not in word1.intersection_points:
                    intersection1 = index1
                    break

            for index2 in indices2:
                if index2 not in word2.intersection_points:
                    intersection2 = index2
                    break

            if (
                intersection1 >= 0
                and intersection2 >= 0
                and intersection1 + intersection2 > 0
            ):
                word1.intersection_points.append(intersection1)
                word2.intersection_points.append(intersection2)
                return (intersection1, intersection2)

        return (-1, -1)


@dataclass
class Grid:
    """Grid class"""

    tree: Tree
    grid: dict[Position, str] = field(init=False, default_factory=dict)
    grid_data: dict[Position, list[Word]] = field(init=False, default_factory=dict)
    ordered_tree: list[tuple[tuple[Word, Word], tuple[int, int]]] = field(
        init=False, default_factory=list
    )
    inserted_words: list[Word] = field(init=False, default_factory=list)

    def __post_init__(self):

        self.create_grid()

        # attempt = 0
        # success = False

        # while not success and attempt < 100:
        #     try:
        #         self.create_grid()
        #         success = True
        #     except ValueError:
        #         if attempt < 100:
        #             attempt += 1
        #             print("Failed to create grid in attempt", attempt)

    def create_grid(self):
        """Creates the grid"""

        self.reorder_tree()
        # print("Tree")
        # print(self.tree.tree)
        # print("Ordered tree")
        # print(self.ordered_tree)

        self.insert_word(self.ordered_tree[0][0][0], Position(0, 0), "A")
        self.inserted_words.append(self.ordered_tree[0][0][0])

        for pair, indices in self.ordered_tree:
            self.insert_words(pair, indices)

        self.normalize_grid()
        # print(self.grid)
        self.draw_grid()
        print("Inserted Words", self.inserted_words)
        print("Number of words inserted", len(self.inserted_words))

    def draw_grid(self):
        """Draws the grid"""

        min_x = min([position.x for position in self.grid])
        max_x = max([position.x for position in self.grid])
        min_y = min([position.y for position in self.grid])
        max_y = max([position.y for position in self.grid])

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                position = Position(x, y)
                if position in self.grid:
                    print(self.grid[position], end=" ")
                else:
                    print(" ", end=" ")
            print()

    def normalize_grid(self):
        """Normalizes the grid"""

        min_x = min([position.x for position in self.grid.keys()])
        min_y = min([position.y for position in self.grid.keys()])

        new_grid = {}
        new_grid_data = {}

        for position, letter in self.grid.items():
            new_position = Position(position.x - min_x, position.y - min_y)
            new_grid[new_position] = letter
            new_grid_data[new_position] = self.grid_data[position]

        self.grid = new_grid
        self.grid_data = new_grid_data

    def insert_words(self, pair: tuple[Word, Word], indices: tuple[int, int]):
        """Inserts the words into the grid"""

        word1, word2 = pair
        index1, index2 = indices

        # inserted_words = []

        # if len(self.grid) == 0:
        #     self.insert_word(word1, Position(0, 0), "A")
        #     inserted_words.append(word1)
        #     # self.insert_words(pair, indices)
        #     print("First word inserted")
        #     return

        if word1 in self.inserted_words and word2 in self.inserted_words:
            return

        if word1 not in self.inserted_words:
            word_to_insert = word1
            base_word = word2
            new_word_index = index1
            base_word_index = index2
        elif word2 not in self.inserted_words:
            word_to_insert = word2
            base_word = word1
            new_word_index = index2
            base_word_index = index1
        else:
            return

        if base_word.direction == "A":
            new_position = Position(
                base_word.position.x + base_word_index,
                base_word.position.y - new_word_index,
            )
            new_direction = "D"
        elif base_word.direction == "D":
            new_position = Position(
                base_word.position.x - new_word_index,
                base_word.position.y + base_word_index,
            )
            new_direction = "A"

        else:
            raise ValueError("Invalid direction")

        self.insert_word(word_to_insert, new_position, new_direction)

    def insert_word(self, word: Word, position: Position, direction: str):
        """Inserts the word into the grid"""

        word.position = position
        word.direction = direction

        grid_copy = self.grid.copy()
        grid_data_copy = self.grid_data.copy()

        for index, letter in enumerate(word.word):
            if direction == "A":
                new_position = Position(position.x + index, position.y)
            elif direction == "D":
                new_position = Position(position.x, position.y + index)
            else:
                raise ValueError("Invalid direction")

            if new_position in self.grid:
                if self.grid[new_position] != letter:
                    self.grid = grid_copy
                    self.grid_data = grid_data_copy
                    return

            self.grid[new_position] = letter
            if new_position in self.grid_data:
                self.grid_data[new_position].append(word)
            else:
                self.grid_data[new_position] = [word]

        self.inserted_words.append(word)

    def reorder_tree(self):
        """Reorders the tree"""

        tree_list = list(self.tree.tree.items())

        ordered_tree = self.ordered_tree.copy()
        # target_word = ""

        for index, item in enumerate(tree_list):
            if index == 0:
                ordered_tree.append(item)
                # target_word = item[0][1]
                continue

            # print(target_word, item)

            # for internal_index, internal_item in enumerate(tree_list):
            for internal_item in tree_list:

                internal_words = set(internal_item[0])

                existing_tuples = list([pair[0] for pair in ordered_tree])
                existing_words = list([word[0] for word in existing_tuples])
                existing_words += list([word[1] for word in existing_tuples])
                existing_words = set(existing_words)

                if existing_words.intersection(internal_words):
                    if internal_item not in ordered_tree:
                        ordered_tree.append(internal_item)

        self.ordered_tree = ordered_tree


def main():
    """Main function"""

    # for word in WORDS:
    #     word_obj = Word(word)
    #     print(word_obj.word)
    #     print(word_obj.letter_indices)
    #     print("==========")

    tree = Tree([Word(word) for word in WORDS])

    # for pair, indices in tree.links.items():
    #     print(pair[0].word, pair[1].word, indices)

    # print("==========")

    # for pair, indices in tree.tree.items():
    #     print(pair[0].word, pair[1].word, indices)

    grid = Grid(tree)
    print(grid.ordered_tree)
    print(len(grid.ordered_tree))
    # print(len(grid.tree.tree))

    print(grid.grid_data)


if __name__ == "__main__":
    main()

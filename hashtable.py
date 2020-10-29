from random import randint
from functools import reduce
from typing import Optional
from veb import VEB
import numpy as np


class RandomTable:
    def __init__(self, table_size=10, word_size=64):
        self.word_size = word_size
        self.table = [int(randint(0, 2 ** (word_size - 1) - 1)) for _ in range(table_size)]

    def get(self, n):
        return self.table[n]


class Element:
    def __init__(self, key: Optional[int] = None, value: Optional[VEB] = None):
        self.key = key
        self.value = value
        self.removed = False

    def is_defined(self) -> bool:
        return self.key is not None

    def remove(self):
        self.key = None
        self.value = None
        self.removed = True


def _init_table(n):
    return [Element() for _ in range(n)]


class Hashtable:
    def __init__(self,
                 table_size: int,
                 word_size=64,
                 binary_piece_size=8,
                 grow_threshold=0.75,
                 shrink_threshold=0.25):
        self._table_size = table_size
        self._filled = 0
        self._binary_piece_size = binary_piece_size
        self._pieces_number = int(word_size / binary_piece_size)
        self._word_size = word_size
        self._removed_count = 0
        self._pieces_table_size = 2 ** self._pieces_number
        self._removed_clean_threshold = 0.25
        self._table = _init_table(table_size)
        self._grow_threshold = grow_threshold
        self._shrink_threshold = shrink_threshold
        self._pieces_tables = [RandomTable(self._pieces_table_size) for _ in range(self._pieces_number)]

    def _get_binary_piece(self, n: int, index: int) -> int:
        offset = self._word_size - (index + 1) * self._binary_piece_size
        return int(n << offset >> (self._word_size - self._binary_piece_size))

    def _split_in_binary_pieces(self, n: int) -> [int]:
        return [self._get_binary_piece(n, i) for i in range(0, self._pieces_number)][::-1]

    def _hash_fn(self, x: int) -> int:
        pieces = self._split_in_binary_pieces(x)
        positions = [self._pieces_tables[i].get(piece) for i, piece in enumerate(pieces)]
        return reduce(lambda a, b: a ^ b, positions)

    def _internal_add(self, key: int, value: VEB) -> int:
        hash_result = self._hash_fn(key)
        offset = 0
        position = (hash_result + offset) % self._table_size
        while self._table[position].is_defined():
            offset += 1
            position = (hash_result + offset) % self._table_size
        self._table[position] = Element(key, value)

        return position

    def add(self, key: int, value: VEB) -> int:
        position = self._internal_add(key, value)
        self._filled += 1

        if (self._filled / self._table_size) > self._grow_threshold:
            self._doubling()

        return position

    def remove(self, key: int) -> None:
        position = self.get(key)

        if position >= 0:
            self._table[position].remove()
            self._removed_count += 1
            self._filled -= 1

            if (self._removed_count / self._table_size) > self._removed_clean_threshold:
                self._clean_removed()

            if (self._filled / self._table_size) < self._shrink_threshold:
                self._halving()

    def get(self, key: int) -> Optional[VEB]:
        hash_result = self._hash_fn(key)
        offset = 0
        position = (hash_result + offset) % self._table_size
        element = self._table[position]

        while (element.removed or element.key != key) and offset < self._table_size:
            position = (hash_result + offset) % self._table_size
            element = self._table[position]
            offset += 1

        return element.value if element.key == key else None

    def _copy(self, old_table):
        for el in old_table:
            if el.key is not None:
                self._internal_add(el.key, el.value)
        self._removed_count = 0

    def _doubling(self):
        old_table = self._table.copy()
        self._table_size = self._table_size * 2
        self._table = _init_table(self._table_size)
        self._copy(old_table)

    def _halving(self):
        old_table = self._table.copy()
        self._table_size = int(self._table_size / 2)
        self._table = _init_table(self._table_size)
        self._copy(old_table)

    def _clean_removed(self):
        old_table = self._table.copy()
        self._table = _init_table(self._table_size)
        self._copy(old_table)

        self._removed_count = 0

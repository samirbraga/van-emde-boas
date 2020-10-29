from math import ceil, floor, sqrt
from typing import Optional, Sequence

ARCH_WORD_SIZE = 64


class VEB(object):
    def __init__(self, w: int = 64):
        from hashtable import Hashtable
        self._w = w
        self._u = 2 ** w - 1
        self.min = None
        self.max = None
        self._summary = None
        self._clusters = Hashtable(table_size=100, word_size=w, binary_piece_size=int(sqrt(w)))

        # binary utilities
        self._max_number = 2 ** w - 1
        self._high_mask = self._max_number >> int(w / 2) << int(w / 2)
        self._low_number = self._max_number >> int(w / 2)

    def _split_number(self, n: int) -> (int, int):
        high = (n & self._high_mask) >> int(self._w / 2)
        low = n & self._low_number
        return high, low

    def _join_number(self, high: int, low: int) -> int:
        return low + (high << int(self._w / 2))

    def insert(self, element: int):
        if self.min is None:
            self.min = self.max = element
        else:
            if element < self.min:
                aux = self.min
                self.min = element
                element = aux

            if element > self.max:
                self.max = element

            if self._u > 2:
                c, i = self._split_number(element)

                node = self._clusters.get(c)
                if node is None:
                    node = VEB(int(self._w / 2))

                    if self._summary is None:
                        self._summary = VEB(int(self._w / 2))
                    self._summary.insert(c)

                node.insert(i)
                self._clusters.add(c, node)

    def successor(self, element: int) -> Optional[int]:
        if self._u <= 2:
            if element == 0 and self.max == 1:
                return 1
            else:
                return None
        elif element < self.min:
            return self.min

        c, i = self._split_number(element)
        cluster = self._clusters.get(c)

        max_c = None

        if cluster is not None:
            max_c = cluster.max

        if max_c is not None and i < max_c:
            return self._join_number(c, cluster.successor(i))
        else:
            successor_cluster = None
            if self._summary is not None:
                successor_cluster = self._summary.successor(i)
            if successor_cluster is None:
                return None
            else:
                _cluster = self._clusters.get(successor_cluster)
                _cluster_min = 0
                if _cluster is not None:
                    _cluster_min = _cluster.min
                return self._join_number(successor_cluster, _cluster_min)

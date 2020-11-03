from __future__ import annotations

from math import ceil, floor, sqrt
from typing import Optional, Sequence

from commands import Cmd
from logger import Logger

ARCH_WORD_SIZE = 64


class VEB:
    min: Optional[int]
    max: Optional[int]

    def __init__(self, w: int = 64, logger: Logger = None):
        self.logger = logger
        from veb_hashtable import Hashtable
        self._w = w
        self._u = 2 ** w
        self._child_w = floor(w / 2)
        self.min = None
        self.max = None
        self._summary = None

        if self._u > 2:
            if self._w > 8:
                self._clusters = Hashtable(100, self._w, 8)
            else:
                self._clusters = Hashtable(100, 8, 8)

        # binary utilities
        self._max_number = 2 ** w - 1
        self._high_mask = self._max_number >> int(w / 2) << int(w / 2)
        self._low_number = self._max_number >> int(w / 2)

    def apply(self, cmd: Cmd, value: int) -> None:
        if cmd == Cmd.INC:
            self.insert(value)
        elif cmd == Cmd.REM:
            self.remove(value)
        elif cmd == Cmd.SUC:
            self.successor(value)
        elif cmd == Cmd.PRE:
            self._internal_predecessor(value)

    def _get_from_clusters(self, key: int) -> Optional[VEB]:
        if self._u <= 2:
            return None
        # if key in self._clusters:
        #     return self._clusters[key]
        # else:
        #     return None
        return self._clusters.get(key)

    def _add_to_clusters(self, key: int, node: VEB):
        # self._clusters[key] = node
        self._clusters.add(key, node)

    def _split_number(self, n: int) -> (int, int):
        high = (n & self._high_mask) >> int(self._w / 2)
        low = n & self._low_number
        # high = int(floor(n / sqrt(self._u)))
        # low = int((n % ceil(sqrt(self._u))))
        return high, low

    def _join_number(self, high: int, low: int) -> int:
        return low + (high << int(self._w / 2))
        # return int((high * floor(sqrt(self._u))) + low)

    def insert(self, element: int):
        if self.member(element):
            return

        if self.logger is not None:
            self.logger.cmd(Cmd.INC, element)

        if self.min is None:
            self.min = self.max = element
        else:
            if element < self.min:
                aux = self.min
                self.min = element
                element = aux

            if self._u > 2:
                c, i = self._split_number(element)

                node = self._get_from_clusters(c)
                if node is None:
                    node = VEB(self._child_w)
                self._add_to_clusters(c, node)

                if self._summary is None:
                    self._summary = VEB(self._child_w)
                if node.min is None:
                    self._summary.insert(c)
                    node.min = i
                    node.max = i
                else:
                    node.insert(i)

            if element > self.max:
                self.max = element

    def successor(self, element: int) -> Optional[int]:
        result = self._internal_successor(element)

        if self.logger is not None:
            self.logger.output(result)

        return result

    def _internal_successor(self, element: int) -> Optional[int]:
        if self.logger is not None:
            self.logger.cmd(Cmd.SUC, element)

        if self._u <= 2:
            if element == 0 and self.max == 1:
                return 1
            else:
                return None
        elif self.min is not None and element < self.min:
            return self.min

        c, i = self._split_number(element)
        cluster = self._get_from_clusters(c)
        max_c = None

        if cluster is not None:
            max_c = cluster.max

        if max_c is not None and i < max_c:
            i_suc = cluster._internal_successor(i)
            if i_suc is None:
                return None
            return self._join_number(c, i_suc)
        else:
            successor_cluster = None
            if self._summary is not None:
                successor_cluster = self._summary._internal_successor(c)
            if successor_cluster is None:
                return None
            _cluster = self._get_from_clusters(successor_cluster)
            _cluster_min = 0
            if _cluster is not None and _cluster.min is not None:
                return self._join_number(successor_cluster, _cluster.min)

        return None

    def predecessor(self, element: int) -> Optional[int]:
        result = self._internal_predecessor(element)

        if self.logger is not None:
            self.logger.output(result)

        return result

    def _internal_predecessor(self, element: int) -> Optional[int]:
        if self.logger is not None:
            self.logger.cmd(Cmd.PRE, element)

        if self._u <= 2:
            if element == 1 and self.min == 0:
                return 0
            else:
                return None
        elif self.max is not None and element > self.max:
            return self.max

        c, i = self._split_number(element)
        cluster = self._get_from_clusters(c)
        min_c = None

        if cluster is not None:
            min_c = cluster.min

        if min_c is not None and i > min_c:
            i_pred = cluster._internal_predecessor(i)
            if i_pred is None:
                return None
            return self._join_number(c, i_pred)
        else:
            pred_cluster = None
            if self._summary is not None:
                pred_cluster = self._summary._internal_predecessor(c)
            if pred_cluster is None:
                if self.min is not None and element > self.min:
                    return self.min
                else:
                    return None
            _cluster = self._get_from_clusters(pred_cluster)
            _cluster_max = 0
            if _cluster is not None and _cluster.max is not None:
                return self._join_number(pred_cluster, _cluster.max)

        return None

    def remove(self, element: int):
        if not self.member(element):
            return

        if self.logger is not None:
            self.logger.cmd(Cmd.REM, element)

        if element == self.min:
            if self._u <= 2 or (self._u > 2 and self._summary is None):
                c = None
            else:
                c = self._summary.min

            if c is None:
                if self.min == self.max:
                    self.max = None
                self.min = None
                return
            cluster = self._get_from_clusters(c)
            if cluster is not None and cluster.min is not None:
                self.min = self._join_number(c, cluster.min)
                element = self.min
        c, i = self._split_number(element)
        cluster = self._get_from_clusters(c)
        if cluster is not None:
            cluster.remove(i)
            if cluster.min is None:
                self._summary.remove(c)
            if self._summary.min is None:
                self.max = self.min
            else:
                _c = self._summary.max
                _cluster = self._get_from_clusters(_c)
                if _cluster is not None and _cluster.max is not None:
                    self.max = self._join_number(_c, _cluster.max)

    def member(self, element: int) -> bool:
        if element == self.min or element == self.max:
            return True
        elif self._u <= 2 or element is None:
            return False
        c, i = self._split_number(element)
        cluster = self._get_from_clusters(c)
        if cluster is None:
            return False
        return cluster.member(i)

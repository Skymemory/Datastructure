import collections.abc
import random
import unittest
from functools import partial

SKIPLIST_MAXLEVEL = 32
SKIPLIST_P = 0.25


def _get_random_level():
    level = 1
    while random.random() < SKIPLIST_P and level < SKIPLIST_MAXLEVEL:
        level += 1
    return level


class _SkipListNode:
    def __init__(self, key, data, level=1):
        self.key = key
        self.data = data
        self.nextp = [None] * level


class SkipList(collections.abc.Mapping):
    def __init__(self):
        self._head = _SkipListNode(None, None, level=SKIPLIST_MAXLEVEL)
        self._level = 1
        self._size = 0

    @property
    def level(self):
        return self._level

    def __getitem__(self, item):
        curr = self._search(item)
        if curr.nextp[0] and curr.nextp[0].key == item:
            return curr.nextp[0].data
        else:
            raise KeyError(f"{item} not found.")

    def __setitem__(self, key, value):
        paths = [None] * SKIPLIST_MAXLEVEL
        curr = self._head

        for level in reversed(range(self.level)):
            while curr.nextp[level] and curr.nextp[level].key < key:
                curr = curr.nextp[level]
            paths[level] = curr

        # if exist, update it
        if curr.nextp[0] and curr.nextp[0].key == key:
            curr.nextp[0].data = value
        else:
            nlevel = _get_random_level()
            if self.level < nlevel:
                for level in range(self.level, nlevel):
                    paths[level] = self._head
                self._level = nlevel

            # allocate new node
            snode = _SkipListNode(key=key, data=value, level=nlevel)
            for level in range(nlevel):
                prev = paths[level]
                snode.nextp[level] = prev.nextp[level]
                prev.nextp[level] = snode

            self._size += 1

    def __delitem__(self, key):
        paths = [None] * SKIPLIST_MAXLEVEL
        curr = self._head

        for level in reversed(range(self.level)):
            while curr.nextp[level] and curr.nextp[level].key < key:
                curr = curr.nextp[level]
            paths[level] = curr

        if curr.nextp[0] and curr.nextp[0].key == key:
            deleted_node = curr.nextp[0]
            for level, next_ in enumerate(deleted_node.nextp):
                paths[level].nextp[level] = next_

                # reset pointer
                deleted_node.nextp[level] = None

            # after delete node, may change self.level decrease, justify it.
            for level in reversed(range(1, self.level)):
                if self._head.nextp[level]:
                    break
                self._level = level

            self._size -= 1

        else:
            raise KeyError(f"{key} not found.")

    def __len__(self):
        return self._size

    def __iter__(self):
        curr = self._head.nextp[0]
        while curr:
            yield curr.key
            curr = curr.nextp[0]

    def __ne__(self, other):
        return NotImplemented

    def __eq__(self, other):
        return NotImplemented

    def _verbose(self):
        """ Debug interface. """
        pprint = partial(print, sep="", end="")
        # visual header
        columns = 1 + (self.level + 1) * 21
        print('-' * columns)
        pprint('|', 'header'.center(columns - 2), '|', end="\n")
        pprint('|', 'level'.center(20), '|')
        for next_ in self._head.nextp:
            if next_ is None:
                break
            pprint(f"{hex(id(next_))}".center(20), "|")
        pprint('\n', '-' * columns, end='\n')

        # visual node
        curr = self._head.nextp[0]
        while curr:
            columns = 1 + (len(curr.nextp) + 1) * 21
            print('-' * columns)
            print('|', f"mid:{hex(id(curr))}".ljust(columns - 2), "|", sep="")
            print("|", f"key:{curr.key}".ljust(columns - 2), "|", sep="")
            pprint("|", "level".center(20), "|")
            for next_ in curr.nextp:
                if next_ is None:
                    pprint("NULL".center(20), "|")
                else:
                    pprint(f"{hex(id(next_))}".center(20), "|")
            pprint("\n", "-" * columns, end="\n")

            curr = curr.nextp[0]

    def _search(self, key):
        curr = self._head

        for level in reversed(range(self.level)):
            while curr.nextp[level] and curr.nextp[level].key < key:
                curr = curr.nextp[level]
        return curr

    def rangekey(self, key1, key2):
        """ return key between key1 and key2(inclusive) """
        less_node = self._search(key1)
        curr = less_node.nextp[0]

        while curr and curr.key <= key2:
            yield curr.key, curr.data
            curr = curr.nextp[0]

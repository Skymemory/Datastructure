import unittest
import random

from skiplist import SkipList


class SkipListTest(unittest.TestCase):
    def setUp(self):
        self.sl = SkipList()

    def test_insert(self):
        key, data = random.randint(0, 1 << 20), 'SkipList'
        self.sl[key] = data

        self.assertEqual(self.sl[key], data)

    def test_remove(self):
        key, data = random.randint(0, 1 << 20), 'SkipList'
        self.sl[key] = data

        self.assertEqual(self.sl[key], data)

        del self.sl[key]

        self.assertRaises(KeyError, self.sl.__getitem__, key)

    def test_update(self):
        key, data = random.randint(0, 1 << 20), 'SkipList'
        self.sl[key] = data
        self.assertEqual(self.sl[key], data)

        self.sl[key] = 'SkyMemory'

        self.assertEqual(self.sl[key], 'SkyMemory')

    def test_search(self):
        key, data = random.randint(0, 1 << 20), 'SkipList'
        self.sl[key] = data

        self.assertEqual(self.sl[key], data)

        self.assertRaises(KeyError, self.sl.__getitem__, key + 1)

    def test_len(self):
        keys = random.sample(range(10000), 50)
        for k in keys:
            self.sl[k] = f"data_{k}"

        self.assertEqual(len(self.sl), len(keys))

    def test_contain(self):
        key, data = 1, 'SkipList'
        self.sl[key] = data

        self.assertIn(1, self.sl)
        self.assertNotIn(2, self.sl)

    def test_iterable(self):
        keys = random.sample(range(10000), 50)
        for k in keys:
            self.sl[k] = f"data_{k}"

        self.assertListEqual(list(self.sl), sorted(keys))

    def test_rangekey(self):
        keys = random.sample(range(10000), 50)
        for k in keys:
            self.sl[k] = f"data_{k}"
        skeys = sorted(keys)
        r1 = self.sl.rangekey(skeys[5], skeys[20])
        r2 = []
        for k in skeys[5:21]:
            r2.append((k, f"data_{k}"))

        self.assertListEqual(list(r1), r2)

    def test_verbose(self):
        keys = random.sample(range(10000), 15)
        for k in keys:
            self.sl[k] = f"data_{k}"
        print()
        self.sl._verbose()


if __name__ == '__main__':
    unittest.main()


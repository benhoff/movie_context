from collections import defaultdict
from copy import deepcopy

class LossyCount:
    def __init__(self, epsilon):
        self._n = 0
        self._count = defaultdict(int)
        self._bucket_id = {}
        self._epsilon =epsilon
        self._current_bucket_id = 1

    def __setitem__(self, key, value):
        self._n += 1
        if key in self._count:
            self._count[key] += value
        else:
            self._count[key] = 1
            self._bucket_id[key] = self._current_bucket_id - 1
        if self._n % (int(1/ self._epsilon)) == 0:
            self._trim()
            self._current_bucket_id += 1


    def __getitem__(self, key):
        return self._count[key]

    def keys(self):
        return self._count.keys()

    def items(self):
        return self._count.items()

    def values(self):
        return self._count.values()

    def _trim(self):
        all_items = deepcopy(self._count)
        for item, value in all_items.items():
            if value <= self._current_bucket_id - self._bucket_id[item]:
                del self._count[item]
                del self._bucket_id[item]

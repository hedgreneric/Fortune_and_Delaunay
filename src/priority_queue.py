from sortedcontainers import SortedKeyList

class IndexedSortedList(SortedKeyList):
    def add(self, value):
        super().add(value)
        self._reindex()  # Reindex after adding

    def pop(self, index):
        value = super().pop(index)
        self._reindex()  # Reindex after popping
        return value

    def remove(self, value):
        super().remove(value)
        self._reindex()  # Reindex after removing

    def _reindex(self):
        # Reindex the elements in the sorted list
        for i, item in enumerate(self):
            item.index = i


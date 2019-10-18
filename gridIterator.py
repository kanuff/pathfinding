class GridIterator:
    # I found myself needing to iterate over all of the spaces in the Grid a lot (mostly when assigning scores to each
    # space) and doing a double for-loop felt clunky, so I quickly added this in once I had everything working and
    # wanted to make the code a little cleaner
    def __init__(self, grid):
        self._items = [item for row in grid for item in row]
        self._index = 0

    def __next__(self):
        if self._index < len(self._items):
            result = self._items[self._index]
            self._index += 1
            return result
        raise StopIteration


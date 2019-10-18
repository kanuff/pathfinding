from space import Space  # this is only imported for testing purposes here
from gridIterator import GridIterator

class Grid:
    def __init__(self, Item, n, m):

        # Like the Space class, I wanted to keep this Grid class as simple as possible as well.
        # All it does is accept an Item object that you want to populate a grid with, and a specified row and col size
        # As it is right now, the Item object it uses to populate the grid must accept two parameters as x and y
        # coordinates, otherwise it'll throw an error and fail to build

        self.rows = n
        self.cols = m
        self.grid = [ [ Item(x, y) for y in range(self.cols) ] for x in range(self.rows) ]

    def __iter__(self):
        return GridIterator(self.grid)

    def valid_space(self, x, y):
        if x < 0 or y < 0: return False
        if x >= self.rows: return False
        if y >= self.cols: return False
        return True

    def display(self):
        for row in range(self.rows):
            print(self.grid[row])

    def show(self, x, y):
        self.grid[x][y].show()  # this method was mostly used to make debugging easier

    def at(self, x, y):
        return self.grid[x][y]


if __name__ == "__main__":
    rows = cols = 5
    grid = Grid(Space, rows, cols)
    grid.display()
    grid.show(3, 4)
    print(grid.at(3, 4))


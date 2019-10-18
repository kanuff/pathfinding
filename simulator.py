from grid import Grid
from space import Space
import numpy as np
import time

class Simulator:
    def __init__(self, grid, start, goal, obstacles = []):
        self.grid = grid
        self.start = grid.at(*start)  # saves item at the starting position
        self.goal = grid.at(*goal)     # saves item at the goal position
        self.obstacles = obstacles
        self.path = []

        # These two methods prepare the simulation so that it's ready to run the aStar algorithm
        self._build_grid()
        self._initialize_nodes()

    def _build_grid(self):
        self._clear_spaces()
        self._place_obstacles()  # Order matters! We need to specify where the obstacles are first so that
        self._build_neighbors()  # the _build_neighbors() method doesn't add them to the list of valid places to travel

    def _initialize_nodes(self):
        self._initialize_parents()
        self._initialize_gscore()
        self._initialize_fscore()

    def _clear_spaces(self):
        for node in self.grid:
            node.obstacle = False

    def _place_obstacles(self):
        for pos in self.obstacles:
            self.grid.at(*pos).obstacle = True

    def _build_neighbors(self):
        MOVEMENT = [
            [1, 0],   # down
            [0, 1],   # right
            [-1, 0],  # up
            [0, -1],   # left
        ]

        # If we wanted to change the allowed movement of the robot, we could just add/replace entries to this list -
        # for example, if we wanted the robot to be able to move along diagonals we could add [1, 1], [1, -1], [-1, 1],
        # and [-1, -1]

        grid = self.grid
        for node in grid:
            neighbors = []
            for direction in MOVEMENT:
                neighbor_pos = np.array(node.pos) + np.array(direction)

                if grid.valid_space(*neighbor_pos) and not grid.at(*neighbor_pos).obstacle:
                    # if the neighbor_pos isn't even on the board it won't bother to check the second half of this
                    # statement, which means we can avoid the potential errors of calling grid.at(x, y)
                    # for an invalid position
                    neighbors.append(grid.at(*neighbor_pos))

                node.neighbors = neighbors

    def _initialize_parents(self):
        for node in self.grid:
            node.parent = None

    def _initialize_gscore(self):
        for node in self.grid:
            node.g = float('inf')
        self.start.g = 0

    def _initialize_fscore(self):
        for node in self.grid:
            node.f = float('inf')
        self.start.f = self._manhattan_distance(self.start, self.goal)

    def _manhattan_distance(self, start_node, end_node):
        return abs(start_node.pos[0] - end_node.pos[0]) + abs(start_node.pos[1] - end_node.pos[1])

    def _get_smallest_f(self, itr):
        return min(itr, key=lambda x: x.f)

    def _travel_cost(self):
        # I set this cost to be just 1 for traveling between two spaces (since we're just moving along cardinals
        # right now) which is probably too simple to have its own function, but I figured we should have
        # an easy way to change the travel cost based off some logic between the nodes if we do need to change it
        # in the future
        return 1

    def _construct_path(self, node):
        path = [node]
        while node.parent:
            path.append(node.parent)
            node = node.parent
        self.path = list(reversed(path))
        return self.path

    def display(self):
        grid = self.grid
        for row in range(grid.rows):
            pretty_row = map(lambda item:  "X" if item.obstacle else
                                           "S" if item == self.start else
                                           "G" if item == self.goal else
                                           "o" if item in self.path else
                                           " ", grid.grid[row])
            print(list(pretty_row))

    def find_path(self):    # This is the A* algorithm
        open_set = {self.start}
        closed_set = set()
        while len(open_set) > 0:
            current_node = self._get_smallest_f(open_set)
            open_set.remove(current_node)
            closed_set.add(current_node)
            for neighbor in current_node.neighbors:
                if neighbor in closed_set: continue
                tentative_gscore = current_node.g + self._travel_cost()
                if tentative_gscore < neighbor.g:
                    neighbor.parent = current_node
                    neighbor.g = tentative_gscore
                    neighbor.f = neighbor.g + self._manhattan_distance(neighbor, self.goal)
                    if neighbor not in open_set:
                        open_set.add(neighbor)
                if neighbor == self.goal:
                    print("PATH FOUND")
                    return self._construct_path(neighbor)
        print("NO PATH POSSIBLE")
        return []

    def get_path(self):
        return list(map(lambda x: x.pos, self.path))


if __name__ == "__main__":
    start_time = time.time()
    rows = cols = 10
    grid = Grid(Space, rows, cols)
    # only takes in the object used to populate the grid, and the size of the grid


    goal = [rows - 1, cols - 1]
    start = [0, 0]
    demo_obstacles = [
        [1, 1],
        [0, 1],
        [2, 1],
        [3, 1],
        [4, 1],
        [rows - 1, int(cols/2)],
        [rows - 2, int(cols/2)],
        [rows - 3, int(cols/2)],
        [rows - 4, int(cols/2)],
        [rows - 5, int(cols/2)],
        [rows - 6, int(cols/2)],
        [1, int(cols/2) - 2],
        [2, int(cols/2) - 2],
        [3, int(cols/2) - 2],
        [4, int(cols/2) - 2],
        [5, int(cols/2) - 2],
        [6, int(cols/2) - 2],
        [rows - 1, cols - 2],
        [rows - 1, cols - 3],
    ]

    sim = Simulator(grid, start, goal, demo_obstacles)
    # we pass the populated grid along with the start, goal, and obstacles array to the simulator.
    # When we create an instance of the Simulator, it will appropriately assign scores to the grid objects
    # in preparation for running the A* algorithm

    sim.display()
    path = sim.find_path()
    sim.display()

    # Once a simulation runs .find_path(), the resulting path gets saved to the instance and can be
    # accessed by calling sim.get_path()

    print(sim.get_path())

    print('Completed in {0} seconds'.format(time.time() - start_time))

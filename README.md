Pathfinding
---
___
#### Design Decisions
The A* algorithm works by assigning an "F score" to valid spaces in 
a given grid that is typically denotated by f(n). A space's F score is then a 
function of two things:
* g(n) - the travel cost between a given space and the starting space
* h(n) - a score describing the distance between the given space and the goal


###### The Space Class
Given with how much information a space on the grid needs to hold, I originally
designed a Space class that would populate a grid and looked something like this:

```python
class Space:
    def __init__(self, x, y, f_score, g_score, h_score, obstacle):
        self.x = x
        self.y = y
        self.f_score = f_score
        self.g_score = g_score
        self.h_score = h_score
        self.obstacle = obstacle
        

```

While something like this would work, it was built to really only work for
the A* algorithm - which is not the only path-finding algorithm. I wanted 
to make something that could be used for a wider set of path-finding implementations,
and changed the Space class to be extremely simple, only keeping track of its position:

```python
class Space:
    def __init__(self, x, y):
        self.pos = [x, y]

```

My thinking was by keeping the Space instances simple, a user could reuse them for different
algorithms and simply define scores/attributes on them as needed when they initialize the Simulator.

This meant moving all of the A* logic into the Simulator class, which I think also helps make
it a little more readable by putting all the relevant processes in one place.

###### The Grid Class
This desire for modularity is also what led to a very simple Grid class:

```python
class Grid:
    def __init__(self, Item, n, m):
        self.rows = n
        self.cols = m
        self.grid = [ [ Item(x,y) for y in range(self.cols) ] for x in range(self.rows) ]
```

This class accepts an object to populate a grid and a shape specification. This lets a user quickly build and populate
a grid while having access to some useful methods that check if a space exists on the grid or to easily
iterate over all the objects in the grid. The only constraint is that the Item used to populate the grid
must accept two parameters in its constructor as x and y coordinates, but otherwise can be swapped out for any custom 
class a user wants.


###### The Simulator
This is where the bulk of the logic happens, and where the entirety of the A* algorithm lives.

Because each Space object has no idea what it's being used for until the simulator uses it, the simulator
calls two methods to prepare the Spaces so that A* can properly process them, and those methods in turn call other
methods in the appropriate order.

```python
class Simulator:
    def __init__(self, grid, start, goal, obstacles = []):
        self.grid = grid
        self.start = grid.at(start[0], start[1])  # saves item at the starting position
        self.goal = grid.at(goal[0], goal[1])     # saves item at the goal position
        self.obstacles = obstacles
        self.path = []

        # These two methods prepare the simulation so that it's ready to run the aStar algorithm
        self._build_grid()
        self._initialize_nodes()
```

I did it this way to make it easier in the future to use the simulator to run different algorithms. If I were to work on
it more, I think a useful thing to build would be to create a class (maybe something 
called PathFinding) that contains different path-finding algorithms that the Simulator would have access to. The
Simulator class would then be changed to accept an 'alg' parameter that specifies what algorithm to use, and then would
build itself and run accordingly.

```pythonstub
import PathFinding as pf
class Simulator:
    def __init__(self, ..., alg='astar'):
        # ...

        # And instead of this
        #self._build_grid()
        #self._initialize_nodes()
        
        # Do something like this
        self.alg = alg
        # and use it with some logic 
        # to call the appropriate
        # methods from PathFinding
```

Doing this would mean the Simulator class could just keep the methods
find_path(), get_path(), and display() where the methods' behavior would change
depending on the value passed in to self.alg.


###### Implementation Details
As it is right now, the robot can only move along the cardinal directions (left, right, up and down). I originally had
it able to move along the diagonals as well, which helped it find shorter paths,
but also led to some unexpected behavior on certain grid configurations as shown below.

![Diagonal Wall Clipping](/imgs/clip_through_walls.jpg)

which on a physical intuition level doesn't feel quite right (since a physical robot would have a width and need some 
kind of minimum clearance between the obstacles to be allowed to make that move). Some things to add in the future would be to create some logic in the _build_neighbors() method to detect if something like that was happening.


___
#### How To Use
The only required library to run the scripts is the _numpy_ library.

Running _python simulator.py_ will run the simulator with the following defaults:
* rows = cols = 10
* start = [0, 0]
* goal = [9, 9]
* obstacles = demo_obstacles

It will print to the console the grid with the starting point, the goal point, and the placed
obstacles, run the A* algorithm to find a path, and then print the grid again with the path
filled in. 

To view the actual path locations, call sim.get_path() and print the result. It will be in order with the starting
location as the first position and the goal location as the last position.


___
#### Future Additions
* [ ] Adding a method to randomly generate an obstacles array. As it is right now, it must be built and passed to the simulator manually
* [ ] Changing the _build_neighbors() method to accept an array of "allowed_directions" to more easily change the behavior of the robot
* [ ] Making the visual output more visual
* [ ] Adding the PathFinder class with other path-finding algorithms and refactoring the Simulator class
* [ ] Adding some checks to make sure that the starting point and the goal point cannot become obstacles
* [ ] Building some CLI to make the simulator easier to run with different parameters

For A*, its time complexity also depends a lot on the heuristic it uses - so I would experiment with ones other than the 
Manhattan distance to see if something else would work better.

___
#### Resources Used
The [Wikipedia page on A*](https://en.wikipedia.org/wiki/A*_search_algorithm) was very helpful in describing the mechanics of the algorithm,
and the pseudocode found there helped a lot in building the find_path() function used in the Simulator class

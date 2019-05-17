import collections

# A solution to a very interesting problem:
# Find the shortest path in a maze from start to finish.
# Input: A rectangular matrix of 1 and 0.
#   1: represents a wall
#   0: represents a corridor
# There is the following extra rule: You can remove 
# exactly one wall -- i.e. you can turn a single 1 into a 0.
#
# Constraints: both height and width are in [2,20]
# Movement is only EW or NS, diagonal moves not allowed
# The maze is guaranteed to have a solution.
#
# Answer: function answer() returns the length of the shortest path.

# Algorithm: Represent the maze as a graph with weighted edges.
# Each passable hallway is a node.  Passable locations are 
# connected with edges.  If 2 areas could be connected
# by removing a wall, then draw an edge, but give it a weight 
# to discourage its use.

#_DEBUG=True
#import FB_3_2_Graph_heatmap as hm

# Bunnynode: Represents a place in the maze a bunny 
# could stand
class BunnyNode:

    WALL_TYPE = 1
    PASSAGE_TYPE = 0
    node_counter=0

    def __init__(self, location, this_type=PASSAGE_TYPE):
        self.location = location
        self.node_type = this_type
        self.node_num = BunnyNode.node_counter
        BunnyNode.node_counter += 1

    def is_wall(self):
        return self.node_type == BunnyNode.WALL_TYPE

    def __str__(self):
        if self.is_wall():
            string = "V" + str(self.node_num) + "[" + str(self.location) + ", W]"
        else:
            string = "V" + str(self.node_num) + "[" + str(self.location) + ", p]"
        return string

    def get_row(self):
        return self.location[0]

    def get_col(self):
        return self.location[1]

    def __hash__(self):
        return self.location[0]*20 + self.location[1]

    def __eq__(self, other):
        return self.location[0] == other.location[0] and self.location[1] == other.location[1]


# The maze represented as a graph with weighted edges
class BunnyMaze:
    """ graph class inspired by https://gist.github.com/econchick/4666413
    """
    # Since largest graph is 20x20, any number larger than 20x20
    # can be considered to be infinite
    dist_infinite = 10**10
    dist_through_wall = 10**5

    def __init__(self, maze_to_use):
        self.vertices = []

        # makes the default value for all vertices an empty list
        self.edges = collections.defaultdict(list)
#        self.weights = {}
        self.height = len(maze_to_use)
        self.width = len(maze_to_use[0])
        self.maze = maze_to_use
        self.wall_penalty=10**2

        self.build_graph_from_maze()

    def add_vertex(self, value):
        # print "adding vertex: " + str(value)
        self.vertices.append(value)

    def add_edge(self, from_vertex, to_vertex, distance):
        if from_vertex == to_vertex: pass  # no cycles allowed
        # Edges are bi-directional, so add both ways
        self.edges[from_vertex].append(to_vertex)
#        self.weights[(from_vertex, to_vertex)] = distance
        self.edges[to_vertex].append(from_vertex)
#        self.weights[(to_vertex, from_vertex)] = distance

    # Sets the current cost of moving through a wall to be x
    def set_wall_penalty(self, x):
        self.wall_penalty = x

    # Returns the cost of moving from between the two vertices
    # if both nodes are non-wall type, then the cost is 1.
    # If one is a wall and the other is not, return the graph's
    # current wall_penalty, as configured by calling
    # self.set_wall_penalty()
    # If both are wall-type, then we should not be here:
    # raise a KeyError
    def get_weight(self, from_vertex, to_vertex):
        # edge = self.weights[(from_vertex, to_vertex)]
        # if not edge:
        #     raise KeyError("There is no edge between nodes" \
        #                    + str(from_vertex) + " and " + str(to_vertex))

        if from_vertex.is_wall() or to_vertex.is_wall():
            return self.wall_penalty
        else:
            return 1

    # Build and return a BunnyGraph object from the argument 'graph'.
    # graph: a NxN array, represented as a list of lists: a list of N rows,
    #         each row is also of length N.
    #         Each row is a list of integers, either 0 or 1.  O represents
    #         passable space, 1 represents a wall.
    # x, y:  The x, y location of the current node that we are adding.
    # Return: A BunnyGraph object.  Edge wights between any two adjacent 0
    #           nodes are always 1.  Weights between nodes of 0 and 1 are
    #           BunnyGraph.through_wall.  Weights between two nodes of type 1
    #           are BunnyGraph.dist_infinite
    def build_graph_from_maze(self):

        curr_row = []

        # Add each row and the edge weights between adjacent nodes
        for row in range(0, self.height):

            # If we're not at the right edge, add the node to the right and
            # the edge to the left.
            for col in range(0, self.width):

                # Make a new node
                curr_type = self.maze[row][col]
                curr_vertex = BunnyNode((row, col), curr_type)
                self.add_vertex(curr_vertex)

                # If this isn't the start of a row, also add the edge to the node to the left
                if col == 0:
                    curr_row = [curr_vertex]

                else:
                    # Not the start of a row: also add edge to left
                    node_to_left = curr_row[-1]
                    edge_weight = 1
                    if curr_type == BunnyNode.WALL_TYPE or node_to_left.is_wall():
                        edge_weight = BunnyMaze.dist_through_wall

                    # No edges between two walls!
                    if not (curr_type == BunnyNode.WALL_TYPE and node_to_left.is_wall()):
                        self.add_edge(node_to_left, curr_vertex, edge_weight)

                    curr_row.append(curr_vertex)

            # Done with this row.  If applicable, add edge weights to row above
            if not row == 0:
                for i in range(0, self.width):
                    node_above = previous_row[i]
                    curr_node = curr_row[i]

                    edge_weight = 1
                    if curr_node.node_type == BunnyNode.WALL_TYPE or node_above.is_wall():
                        edge_weight = BunnyMaze.dist_through_wall

                    if not (curr_node.node_type == BunnyNode.WALL_TYPE and node_above.is_wall()):
                        self.add_edge(node_above, curr_node, edge_weight)

            previous_row = curr_row

    def print_graph(self):
        last_row = 0
        string = ""
        for n in self.vertices:
            if n.get_row() != last_row:
                print string
                string = ""
                last_row = n.get_row()
            string += str(n) + " "

        print string


        for e in self.edges.keys():
            for to in self.edges[e]:
                string = "Edge from " + str(e) + " to " + str(to) + ": weight=" + str(self.get_weight((e, to)))

                print string

    def __str__(self):
        string = "Vertices: " + str(self.vertices) + "\n"
        string += "Edges: " + str(self.edges) + "\n"
#        string += "Weights: " + str(self.weights)
        return string

    def dijkstra(self, start):
        # S will be the vertices that we have already visited.
        S = set()
        try:
            global _DEBUG
            _DEBUG
        except NameError:
            _DEBUG = False

        if _DEBUG:
            import time
            heatmap = hm.GraphHeatmap(self.maze)

        # delta: a dictionary of the length of the shortest distance to each
        #       node, from start.
        #        key=node (a BunnyNode object), value = (int) distance from Start
        # We initialize it so that every vertex has a path of infinity
        delta = dict.fromkeys(list(self.vertices), BunnyMaze.dist_infinite)
        previous = dict.fromkeys(list(self.vertices), None)

        # then we set the path length of the start vertex to 0
        delta[start] = 0

        # while there exists a vertex v that we haven't visited (not in S)
        vertex_set = set(self.vertices)
        while S != vertex_set:
            # let v be the closest vertex that has not been visited...it will begin at 'start'
            v = min((set(delta.keys()) - S), key=delta.get)
            if _DEBUG:
                heatmap.set_working_node(v.get_row(), v.get_col())

            # for each neighbor of v not in S
            for neighbor in set(self.edges[v]) - S:
                new_path_weight = delta[v] + self.get_weight(v, neighbor)

                # is the new path from neighbor through
                if new_path_weight < delta[neighbor]:
                    # since it's optimal, update the shortest path for neighbor
                    if _DEBUG:
                        heatmap.shade_from_path_weight(neighbor.get_row(), neighbor.get_col(), new_path_weight)
                        time.sleep(1)
                    delta[neighbor] = new_path_weight

                    # set the previous vertex of neighbor to v
                    previous[neighbor] = v
            S.add(v)

        return (delta, previous)

    def shortest_path(self, start, end):
        """Uses dijkstra function in order to output the shortest path from start to end
        """

        delta, previous = self.dijkstra(start)

        escape_path = BunnyPath(self)
        vertex = end

        while vertex is not None:
            escape_path.add_node(vertex)
            vertex = previous[vertex]

        escape_path.reverse()
        return escape_path

    # Return the shortest path between the vertices start and end, setting
    # the penalty for crossing a wall to be 2 * wall_penalty
    def min_path_with_wall_penalty(self, start, end, wall_penalty):

        self.set_wall_penalty(wall_penalty)
        path = self.shortest_path(start, end)

        # Three possibilities:
        # * There are no walls in the path.  This must be the correct path.
        # * There is exactly one wall in the path.  Then this must be the correct path.
        # * There is more than 1 walls in the path.  In this case, we're going create a
        #   very high wall penalty, then go through the path, removing exactly one wall
        #   at a time, to see which wall gives us the shortest path.
        walls = path.count_walls()
        if walls < 2:
            return path

        savepath = None

        self.set_wall_penalty(10**3)

        # One at a time, take out the walls and find the shortest path.  If the
        # new shortest path still has a wall in it, then this path is no good.
        for node in path.path:
            if (node.is_wall()):
                node.node_type = BunnyNode.PASSAGE_TYPE
                newpath = path.make_new_exit_path()
                if newpath.count_walls() != 0:
                    node.node_type = BunnyNode.WALL_TYPE
                    continue

                if not savepath:
                    savepath = newpath
                elif newpath.length() < savepath.length():
                    savepath = newpath
                node.node_type = BunnyNode.WALL_TYPE

        w = savepath.count_walls()
        if (w > 1):
            print "Failure: returning this path, which has " + str(w) + " walls"
            print w
            raise AssertionError("min_path_with_wall_penalty returning path with walls="+ str(w))

        self.set_wall_penalty(wall_penalty)
        return savepath

# A pathway through the graph from (0,0) to (n,m) (upper left
# to bottom right.
class BunnyPath:

    def __init__(self, in_graph):
        self.path = []
        self._walls = 0
        self.graph = in_graph

    def add_node(self, node):
        self.path.append(node)
        if (node.is_wall()):
            self._walls += 1

    def reverse(self):
        self.path.reverse()

    def count_walls(self):
        if not self._walls == None:
            return self._walls

        self._walls = 0
        for n in self.path:
            if n.node_type == BunnyNode.WALL_TYPE:
                self._walls += 1

        return self._walls

    def num_nodes(self):
        return len(self.path)

    def path_weight(self):
        lastnode = None
        weight = 0
        for node in self.path:
            if lastnode:
                weight += self.graph.get_weight(lastnode, node)

            lastnode = node

        return weight

    def as_list(self):
        return self.path

    def length(self):
        return len(self.path)

    def __len__(self):
        return len(self.path)

    def __str__(self):
        if (self.length()):
            string = str(self.path[0])
        else:
            string = ""

        for node in self.path[1:]:
            string += " -> " + str(node)

        return string

    # Return a sub_path of this path, starting from index, and going
    # to the end of the path.
    # Equivalent to list[index:]
    def sub_path_from_index(self, index):
        new_sub_path = BunnyPath(self.graph)
        new_sub_path.path = self.path[index:]
        new_sub_path._walls = None  # walls must be re-counted when accessed
        return new_sub_path

    # Return a sub_path of this path, starting from the beginning, and ending at
    # index - 1, but not including the node at index.
    # Equivalent to list[0:index]
    # to the end of the path.  This is equivalent to a slice of a list.
    def sub_path_to_index(self, index):
        new_sub_path = BunnyPath(self.graph)
        new_sub_path.path = self.path[:index]
        new_sub_path._walls = None  # walls must be re-counted when accessed
        return new_sub_path

    # Create a new path object with same start and end nodes as this one
    # May be different than this one if the underlying graph parameters
    # have changed.
    def make_new_exit_path(self):
        start = self.path[0]
        end = self.path[-1]
        newpath = self.graph.shortest_path(start, end)
        return newpath


    # Compare this path with the argument.  We are looking for places where
    # there are segments in both paths that differ from each other.
    # The two paths (this and the argument) must have the same start and end nodes.
    # returns: A list of NamedTuples, being the indexes of the diverge/convere
    #           nodes in each of the paths.
    #          NamedTuple:  ("SubPath", "divergeA convergeA divergeB convergeB")
    #           The subpaths in the list returned are guaranteed to be in order
    #            from closest to the beginning of the paths.
    def find_divergent_subpaths(self, other_path):

        # pathA and pathB must be two paths with a common start node
        # return two subpaths of each, with the first node of each
        # being node that they have in common before they diverge.
        # If the paths don't diverge, or one is shorter than the other,
        # return (None, None)
        def find_diverge_point(pathA, pathB):
            index = 0
            result = None, None

            # If we're out of path, just return
            if (len(pathA) == 0 or len(pathB) == 0):
                return result

            while True:
                index += 1
                if index == pathA.length() or index == pathB.length():
                    break

                if pathA.path[index] != pathB.path[index]:
                    index -=1
                    result = pathA.sub_path_from_index(index), pathB.sub_path_from_index(index)
                    break

            return result

        # Args: two paths that have the same start node, but that diverge
        # after that.  At some point in their lengths they will converge.
        # Create two new paths, both of which end at the nodes where the
        # two argument paths first converge.
        def cut_paths_at_convergence(pathA, pathB):
            if len(pathA) < 2 or len(pathB) < 2:
                raise AssertionError("cut_paths_at_convergence called with paths of length" \
                                     + str(len(pathA)) + " and " + str(len(pathB)))

            indexA, indexB = 0, 0
            for n in pathB.path[1:]:
                indexB += 1
                if n in pathA.path:
                    indexA = pathA.path.index(n)
                    clipped_subpathA = pathA.sub_path_to_index(indexA+1)
                    clipped_subpathB = pathB.sub_path_to_index(indexB + 1)
                    break

            if indexA == 0:
                raise AssertionError("cut_paths_at_convergence: paths do not appear to converge")

            return clipped_subpathA, clipped_subpathB

        result=[]
        subA, subB = find_diverge_point(self, other_path)
        if not subA:
            print "Paths did not diverge"
        while subA:
            clippedA, clippedB = cut_paths_at_convergence(subA, subB)
            result.append((clippedA, clippedB))

            # Now skip to the end of our clipped path and repeat until we
            # find no more divergent subpaths in A or B
            pathA_skip = len(clippedA)
            pathB_skip = len(clippedB)
            subA = subA.sub_path_from_index(pathA_skip)
            subB = subB.sub_path_from_index(pathB_skip)
            subA, subB = find_diverge_point(subA, subB)

        return result


def answer_path(map):
    graph = BunnyMaze(map)
    #    graph.print_graph()
    h, w = len(map), len(map[0])
    start = BunnyNode((0, 0), 0)
    end = BunnyNode((h-1, w-1), 0)

    # Iterate over various amounts of initial wall penalty to find the initial
    # multi-wall path, then the function min_path_with_wall_penalty will optimize
    # that path for only 1 wall removed.
    bestlen = 10**4
    bestpath = None
    for wp in [20]:
        print "Trying with wall penalty = " + str(wp)
        mp = graph.min_path_with_wall_penalty(start, end, wp)

        # If this didn't produce a valid path, try with the next wall penalty
        if not mp:
            continue

        if mp.length() < bestlen:
            bestlen = mp.length()
            bestpath = mp

    if not bestpath:
        raise AssertionError("No exit path found!")

    return bestpath

def answer(map):
    return answer_path(map).length()

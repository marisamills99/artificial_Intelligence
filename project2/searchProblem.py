# searchProblem.py - representations of search problems
# AIFCA Python3 code Version 0.7.9 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from pacman import *
import inspect
import time


class Search_problem(object):
    """A search problem consists of:
    * a start node
    * a neighbors function that gives the neighbors of a node
    * a specification of a goal
    * a (optional) heuristic function.
    The methods must be overridden to define a search problem."""
    def __init__(self, maze, cost=lambda n: 1, heuristic=None):
        print(cost, heuristic)
        self.maze = maze
        self.explored = set()
        self.cost = cost
        #print('heuristics: ',heuristic,'   cost:', cost)
        if (heuristic==None):
            self.heuristic = lambda n: 0
        elif heuristic=='h1':
            self.heuristic = lambda n: len(n[1])
        elif heuristic=='h2':
            self.heuristic = self.heuristicManhattan
        elif heuristic=='cornersHeuristic':
            self.heuristic = self.heuristicCorners
        elif heuristic=='foodHeuristic':
            self.heuristic = self.heuristicFood
        else:
            self.heuristic = lambda n: 0
    
    def start_node(self):
        """returns start node"""
        # print('start = ',self.maze.state)
        return self.maze.state
        #raise NotImplementedError("start_node")   # abstract method
    
    def is_goal(self,node):
        """is True if node is a goal"""
        return (len(node[1])==0)
        #raise NotImplementedError("is_goal")   # abstract method
    
    def neighbors(self,node):
        """returns a list of the arcs for the neighbors of node"""
        _pos = node[0]
        _legal = self.maze.legalMoves(node[0])
        _neighbors = []
        for _dir in _legal:
            _food = node[1].copy()
            _power = node[2].copy()
            _newpos = self.maze.makeMove(_pos,_dir)
            if (_newpos in _food):
                _food.remove(_newpos)
            elif (_newpos in _power):
                _power.remove(_newpos)
            _neighbors.append([[_newpos,_food,_power], self.cost(_newpos)]) # add cost to end, note the difference with explicit graph search
        return _neighbors
        #raise NotImplementedError("neighbors")   # abstract method
    
    def heuristicManhattan(self,n):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""
        _pos = n[0]
        if (len(n[1])==0):
            return 0
        _foodpos = n[1][0]    # n[1] is the list of all food items
        # Manhattan distance between the food and the current pacman position,
        # works for single food item search
        i=0
        while i<len(n[1]):
            _food= n[1][i]
            if (abs(_pos[0]-_food[0])+abs(_pos[1]-_food[1])) > (abs(_pos[0]-_foodpos[0])+abs(_pos[1]-_foodpos[1])):
                _foodpos= _food
            i+=1
        return abs(_pos[0]-_foodpos[0])+abs(_pos[1]-_foodpos[1])
    
    def nullHeuristic(self,n):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""
        return 0
    
    def heuristicCorners(self, n):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""
         
        x= self.heuristicManhattan(n)
        return x

    def heuristicFood(self, n):
        n_pos=n[0]
        n_foodList=n[1]
        x= self.heuristicManhattan(n)
        return x


class Arc(object):
    """An arc has a from_node and a to_node node and a (non-negative) cost"""
    def __init__(self, from_node, to_node, cost=1, action=None):
        assert cost >= 0, ("Cost cannot be negative for"+
                           str(from_node)+"->"+str(to_node)+", cost: "+str(cost))
        self.from_node = from_node
        self.to_node = to_node
        self.action = action
        self.cost=cost

    def __repr__(self):
        """string representation of an arc"""
        if self.action:
            return str(self.from_node)+" --"+str(self.action)+"--> "+str(self.to_node)
        else:
            return str(self.from_node)+" --> "+str(self.to_node)

class Search_problem_from_explicit_graph(Search_problem):
    """A search problem consists of:
    * a list or set of nodes
    * a list or set of arcs
    * a start node
    * a list or set of goal nodes
    * a dictionary that maps each node into its heuristic value.
    """

    def __init__(self, nodes, arcs, start=None, goals=set(), hmap={},):
        self.neighs = {}
        self.nodes = nodes
        for node in nodes:
            self.neighs[node]=[]
        self.arcs = arcs
        for arc in arcs:
            self.neighs[arc.from_node].append([arc.to_node, arc.cost])
        self.start = start
        self.goals = goals
        self.hmap = hmap
        self.explicit = 1

    def start_node(self):
        """returns start node"""
        return self.start
    
    def is_goal(self,node):
        """is True if node is a goal"""
        return node in self.goals

    def neighbors(self,node):
        """returns the neighbors of node"""
        return self.neighs[node]

    def heuristic(self,node):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden in the hmap."""
        if node in self.hmap:
            return self.hmap[node]
        else:
            return 0
        
    def __repr__(self):
        """returns a string representation of the search problem"""
        res=""
        for arc in self.arcs:
            res += str(arc)+".  "
        return res

    def neighbor_nodes(self,node):
        """returns an iterator over the neighbors of node"""
        return (path.to_node for path in self.neighs[node])

class Path(object):
    """A path is either a node or a path followed by an arc"""
    
    def __init__(self,initial,arc=None):
        """initial is either a node (in which case arc is None) or
        a path (in which case arc is an object of type Arc)"""
        self.initial = initial
        self.arc=arc
        if arc is None:
            self.cost=0
        else:
            #print(arc)
            self.cost = initial.cost+arc[1]

    def end(self):
        """returns the node at the end of the path"""
        if self.arc is None:
            return self.initial
        else:
            return self.arc[0]

    def nodes(self):
        """enumerates the nodes for the path.
        This starts at the end and enumerates nodes in the path backwards."""
        current = self
        while current.arc is not None:
            yield current.arc[0]
            current = current.initial
        yield current.initial

    def initial_nodes(self):
        """enumerates the nodes for the path before the end node.
        This starts at the end and enumerates nodes in the path backwards."""
        if self.arc is not None:
            for nd in self.initial.nodes(): yield nd     # could be "yield from"
        
    def __repr__(self):
        """returns a string representation of a path"""
        if self.arc is None:
            return str(self.initial)
        else:
            return str(self.initial)+" --> "+str(self.arc[0])

problem1 = Search_problem_from_explicit_graph(
    {'a','b','c','d','g'},
    [Arc('a','b',1), Arc('a','c',3), Arc('b','d',3), Arc('b','c',1),
        Arc('c','d',1), Arc('c','g',3), Arc('d','g',1)],
    start = 'a',
    goals = {'g'})

problem2 = Search_problem_from_explicit_graph(
    {'a','b','c','d','e','g','h','j'},
    [Arc('a','b',1), Arc('b','c',3), Arc('b','d',1), Arc('d','e',3),
        Arc('d','g',1), Arc('a','h',3), Arc('h','j',1)],
    start = 'a',
    goals = {'g'})

problem3 = Search_problem_from_explicit_graph(
    {'a','b','c','d','e','g','h','j'},
    [],
    start = 'g',
    goals = {'k','g'})

acyclic_delivery_problem = Search_problem_from_explicit_graph(
    {'mail','ts','o103','o109','o111','b1','b2','b3','b4','c1','c2','c3',
     'o125','o123','o119','r123','storage'},
     [Arc('ts','mail',6),
        Arc('o103','ts',8),
        Arc('o103','b3',4),
        Arc('o103','o109',12),
        Arc('o109','o119',16),
        Arc('o109','o111',4),
        Arc('b1','c2',3),
        Arc('b1','b2',6),
        Arc('b2','b4',3),
        Arc('b3','b1',4),
        Arc('b3','b4',7),
        Arc('b4','o109',7),
        Arc('c1','c3',8),
        Arc('c2','c3',6),
        Arc('c2','c1',4),
        Arc('o123','o125',4),
        Arc('o123','r123',4),
        Arc('o119','o123',9),
        Arc('o119','storage',7)],
    start = 'o103',
    goals = {'r123'},
    hmap = {
        'mail' : 26,
        'ts' : 23,
        'o103' : 21,
        'o109' : 24,
        'o111' : 27,
        'o119' : 11,
        'o123' : 4,
        'o125' : 6,
        'r123' : 0,
        'b1' : 13,
        'b2' : 15,
        'b3' : 17,
        'b4' : 18,
        'c1' : 6,
        'c2' : 10,
        'c3' : 12,
        'storage' : 12
        }
    )

cyclic_delivery_problem = Search_problem_from_explicit_graph(
    {'mail','ts','o103','o109','o111','b1','b2','b3','b4','c1','c2','c3',
     'o125','o123','o119','r123','storage'},
     [  Arc('ts','mail',6), Arc('mail','ts',6),
        Arc('o103','ts',8), Arc('ts','o103',8),
        Arc('o103','b3',4), 
        Arc('o103','o109',12), Arc('o109','o103',12),
        Arc('o109','o119',16), Arc('o119','o109',16),
        Arc('o109','o111',4), Arc('o111','o109',4),
        Arc('b1','c2',3),
        Arc('b1','b2',6), Arc('b2','b1',6),
        Arc('b2','b4',3), Arc('b4','b2',3),
        Arc('b3','b1',4), Arc('b1','b3',4),
        Arc('b3','b4',7), Arc('b4','b3',7),
        Arc('b4','o109',7), 
        Arc('c1','c3',8), Arc('c3','c1',8),
        Arc('c2','c3',6), Arc('c3','c2',6),
        Arc('c2','c1',4), Arc('c1','c2',4),
        Arc('o123','o125',4), Arc('o125','o123',4),
        Arc('o123','r123',4), Arc('r123','o123',4),
        Arc('o119','o123',9), Arc('o123','o119',9),
        Arc('o119','storage',7), Arc('storage','o119',7)],
    start = 'o103',
    goals = {'r123'},
    hmap = {
        'mail' : 26,
        'ts' : 23,
        'o103' : 21,
        'o109' : 24,
        'o111' : 27,
        'o119' : 11,
        'o123' : 4,
        'o125' : 6,
        'r123' : 0,
        'b1' : 13,
        'b2' : 15,
        'b3' : 17,
        'b4' : 18,
        'c1' : 6,
        'c2' : 10,
        'c3' : 12,
        'storage' : 12
        }
    )
def ManhattanDist(pacman_pos,_food):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""
        return abs(pacman_pos[0]-_food[0])+abs(pacman_pos[1]-_food[1])

def FindClosestDot(pacman_pos, food):
    _closest = food[0]
    _mindist = ManhattanDist(pacman_pos, food[0])
    for _food in food[1:]:
        _dist = ManhattanDist(pacman_pos, _food)
        if _dist < _mindist:
            _mindist = _dist
            _closest = _food
    return _closest
    

def findPathToClosestDot(problem, pacman_pos, closest):
    """
    You need to implement the problem.maze.state and the search call
    """
    from searchGeneric import AStarSearcher
	#import searcher to create a food problem then search 
    problem.maze.state[0] = pacman_pos
    problem.maze.state[1] = [closest]
    maze = problem.maze 
    closestDotSearch = AStarSearcher(Search_problem(maze, lambda n:1, 'foodHeuristic'))
    return closestDotSearch.search() 


def ClosestDotSearchAgent(problem):
    from runPacman import getNodes
    _food = problem.maze.food
    _power = problem.maze.power
    _pacman_pos = problem.maze.pacman_pos
    _cost = 0
    _full_path = [_pacman_pos]
    _explored = _full_path
    while len(_food) > 0:
        _closest = FindClosestDot(_pacman_pos, _food)
        _path, _explored1 = findPathToClosestDot(problem, _pacman_pos, _closest)
        path = getNodes(_path)
        _cost = _cost + len(path) - 1
        for _p in path[1:]:
            if _p in _food:
                _food.remove(_p)
        _full_path = _full_path + path[1:]
        _explored = _explored + _explored1
        _pacman_pos = _closest
    print('Total past cost is ',_cost)
    return _full_path, _explored

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" % (method, line, fileName))
    sys.exit(1)
# searchGeneric.py - Generic Searcher, including depth-first and A*
# AIFCA Python3 code Version 0.7.9 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from display import Displayable, visualize
import searchProblem

class Searcher(Displayable):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    This does depth-first search unless overridden
    """
    def __init__(self, problem, quiet=False):
        """creates a searcher from a problem
        """
        self.quiet = quiet
        self.problem = problem
        self.initialize_frontier()
        self.num_expanded = 0
        self.explored_nodes = []
        self.add_to_frontier(Path(problem.start_node()))
        super().__init__()

    def initialize_frontier(self):
        self.frontier = []
        
    def empty_frontier(self):
        return self.frontier == []
        
    def add_to_frontier(self,path):
        self.frontier.append(path)
        
    @visualize
    def search(self):
        """returns (next) path from the problem's start node
        to a goal node. 
        Returns None if no path exists.
        """
        self.explored={}
        while not self.empty_frontier():
            path = self.frontier.pop()
            #if path.end() not in self.explored:
            # need to add checking if the path has already been explored
            # add the current state in the has table
            # update the explored nodes
            #self.explored_nodes.append(node[0])
            self.display(2, "Expanding:",path,"(cost:",path.cost,")")
            self.num_expanded += 1
            #print(self.problem.maze.state)
            if self.problem.is_goal(path.end()):    # solution found
                if not self.quiet:
                       self.display(1, self.num_expanded, "paths have been expanded and",
                                        len(self.frontier), "paths remain in the frontier")
                self.solution = path   # store the solution found
                return path, self.explored_nodes
            else:
                neighs = self.problem.neighbors(path.end())
                self.display(3,"Neighbors are", neighs)
                #print(neighs)
                # you should not use arcs, but nodes only
                for arc in neighs:
                    #print("path is \n\n", path)
                    #self.explored_nodes.append(arc[0][0])
                    node=""
                    node+=str(arc[0][0])
                    node+=str(arc[0][1])
                    node+=str(arc[0][2])
                    #print("Node is \n\n",node)
                    if node not in self.explored :
                        self.explored_nodes.append(arc[0][0])
                        self.add_to_frontier(Path(path,arc))
                        #if not at food goals 
                        self.explored[node]=""
                    #self.explored_nodes.append(arc[1])
                self.display(3,"Frontier:",self.frontier)
        return path, self.explored_nodes
        self.display(1,"No (more) solutions. Total of",
                     self.num_expanded,"paths expanded.")
import queue
class FrontierQ(object):
    def __init__(self):
        """constructs the frontier, initially an empty queue 
        """
        self.frontier_index = 0  # the number of items ever added to the frontier
        self.frontierq = []  # the frontier queue

    def empty(self):
        """is True if the queue is empty"""
        return self.frontierq == []
    
    def add(self, path, value):
        """add a path to the priority queue
        value is the value to be minimized"""
        self.frontier_index += 1    # get a new unique index
        queue.heappush(self.frontierq,(value, -self.frontier_index, path))

    def pop(self):
        """returns and removes the path of the frontier with minimum value.
        """
        (_,_,path) = queue.heappop(self.frontierq)
        return path
    
    def __len__(self):
        """length of the frontier"""
        return len(self.frontierq)

    def __iter__(self):
        """iterate through the paths in the frontier"""
        for (_,_,path) in self.frontierq:
            yield path


    def count(self,val):
        """returns the number of elements of the frontier with value=val"""
        return sum(1 for e in self.frontierq if e[0]==val)

import heapq        # part of the Python standard library
from searchProblem import Path

class FrontierPQ(object):
    """A frontier consists of a priority queue (heap), frontierpq, of
        (value, index, path) triples, where
    * value is the value we want to minimize (e.g., path cost + h).
    * index is a unique index for each element
    * path is the path on the queue
    Note that the priority queue always returns the smallest element.
    """

    def __init__(self):
        """constructs the frontier, initially an empty priority queue 
        """
        self.frontier_index = 0  # the number of items ever added to the frontier
        self.frontierpq = []  # the frontier priority queue

    def empty(self):
        """is True if the priority queue is empty"""
        return self.frontierpq == []

    def add(self, path, value):
        """add a path to the priority queue
        value is the value to be minimized"""
        self.frontier_index += 1    # get a new unique index
        heapq.heappush(self.frontierpq,(value, -self.frontier_index, path))

    def pop(self):
        """returns and removes the path of the frontier with minimum value.
        """
        (_,_,path) = heapq.heappop(self.frontierpq)
        return path 

    def count(self,val):
        """returns the number of elements of the frontier with value=val"""
        return sum(1 for e in self.frontierpq if e[0]==val)

    def __repr__(self):
        """string representation of the frontier"""
        return str([(n,c,str(p)) for (n,c,p) in self.frontierpq])
    
    def __len__(self):
        """length of the frontier"""
        return len(self.frontierpq)

    def __iter__(self):
        """iterate through the paths in the frontier"""
        for (_,_,path) in self.frontierpq:
            yield path

class BFSearcher(Searcher):
    """ Returns Breadth First searcher for a problem
        Overload some files - the least number required
    """
    def __init__(self, problem, quiet=False):
        """creates a searcher from a problem
        """
        self.quiet = quiet
        self.problem = problem
        self.initialize_frontier()
        self.num_expanded = 0
        self.explored_nodes = []
        self.add_to_frontier(Path(problem.start_node()))
        

    def initialize_frontier(self):
        self.frontier = []
        
    def empty_frontier(self):
        return self.frontier == []
        
    def add_to_frontier(self,path):
        self.frontier.append(path)
      
    def search(self):
        """returns (next) path from the problem's start node
        to a goal node. 
        Returns None if no path exists.
        """
        self.explored={}
        while not self.empty_frontier():
            path = self.frontier.pop(0)
            self.display(2, "Expanding:",path,"(cost:",path.cost,")")
            self.num_expanded += 1
            #print(self.problem.maze.state)
            if self.problem.is_goal(path.end()):    # solution found
                if not self.quiet:
                       self.display(1, self.num_expanded, "paths have been expanded and",
                                        len(self.frontier), "paths remain in the frontier")
                self.solution = path   # store the solution found
                return path, self.explored_nodes
            else:
                neighs = self.problem.neighbors(path.end())
                self.display(3,"Neighbors are", neighs)
                #print(neighs)
                # you should not use arcs, but nodes only
                for arc in reversed(list(neighs)):
                    #print("path is \n\n", path)
                    node=""
                    node+=str(arc[0][0])
                    node+=str(arc[0][1])
                    node+=str(arc[0][2])
                    #print("Node is \n\n",node)
                    if node not in self.explored :
                        self.explored_nodes.append(arc[0][0])
                        self.add_to_frontier(Path(path,arc))
                        #if not at food goals 
                        self.explored[node]=""
                    #self.explored_nodes.append(arc[1])
                self.display(3,"Frontier:",self.frontier)
        return path, self.explored_nodes
        self.display(1,"No (more) solutions. Total of",
                     self.num_expanded,"paths expanded.")
    
class AStarSearcher(Searcher):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    """

    def __init__(self, problem):
        super().__init__(problem)

    def initialize_frontier(self):
        self.frontier = FrontierQ()

    def empty_frontier(self):
        return self.frontier.empty()

    def add_to_frontier(self,path):
        """add path to the frontier with the appropriate cost"""
        value = path.cost+self.problem.heuristic(path.end())
        self.frontier.add(path, value)

class UniformCostSearcher(Searcher):
    """returns a searcher for a problem.
       Paths can be found by repeatedly calling search().
       Overload some files, the least number required. Look at AStarSearcher class.
       use a queue not priority queue
    """
    def __init__(self, problem):
        super().__init__(problem)

    def initialize_frontier(self):
        self.frontier = FrontierPQ()

    def empty_frontier(self):
        return self.frontier.empty()

    def add_to_frontier(self,path):
        """add path to the frontier with the appropriate cost"""
        value = path.cost
        self.frontier.add(path, value)

from searchProblem import *

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
    return raiseNotDefined()
        
def ClosestDotSearchAgent(problem):
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

def test(SearchClass, problem=searchProblem.problem1, solution=['g','d','c','b','a'] ):
    """Unit test for aipython searching algorithms.
    SearchClass is a class that takes a problemm and implements search()
    problem is a search problem
    solution is the unique (optimal) solution. 
    """
    print("Testing problem 1:")
    schr1 = SearchClass(problem)
    path1 = schr1.search()
    print("Path found:",path1)
    assert list(path1.nodes()) == solution, "Shortest path not found in problem1"
    print("Passed unit test")

if __name__ == "__main__":
    #test(Searcher)
    test(AStarSearcher)
    
# example queries:
#searcher1 = Searcher(searchProblem.acyclic_delivery_problem)   # DFS
#searcher1.search()  # find first path
#searcher1.search()  # find next path
# searcher2 = AStarSearcher(searchProblem.acyclic_delivery_problem)   # A*
# searcher2.search()  # find first path
# searcher2.search()  # find next path
# searcher3 = Searcher(searchProblem.cyclic_delivery_problem)   # DFS
# searcher3.search()  # find first path with DFS. What do you expect to happen?
#searcher4 = Searcher(searchProblem.cyclic_delivery_problem)    # A*
#searcher4.search()  # find first path

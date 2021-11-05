# cspProblem.py - Representations of a Constraint Satisfaction Problem
# AIFCA Python3 code Version 0.8.2 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
from operator import lt,ne,eq,gt
def ne_(val):
    """not equal value"""
    # nev = lambda x: x != val   # alternative definition
    # nev = partial(neq,val)     # another alternative definition
    def nev(x):
        return val != x
    nev.__name__ = str(val)+"!="      # name of the function 
    return nev
def safeSpace(key,key2):
    #p1 and p2 are tuples that have (row,column)
    differenceRow= abs(key[0]-key2[0])
    differenceColumn=abs(key[1]-key2[1])
    if differenceRow is not 0:
        if differenceColumn is not 0:
            if differenceRow is not differenceColumn:
                return True
    return False
def safeDiagonal(differenceRow):
    def nev(queen_col,queen2_col):
        #differenceRow= abs(int(queen_row)-int(queen2_row))
        differenceColumn=abs(int(queen_col)-int(queen2_col))
        return differenceRow != differenceColumn
    nev.__name__ = str((differenceRow))+"!="      # name of the function 
    return nev
    
class Constraint(object):
    """A Constraint consists of
    * scope: a tuple of variables
    * condition: a function that can applied to a tuple of values
    * string: a string for printing the constraints. All of the strings must be unique.
    for the variables
    """
    def __init__(self, scope, condition, string=None):
        self.scope = scope
        self.condition = condition
        if string is None:
            self.string = self.condition.__name__ + str(self.scope)
        else:
            self.string = string

    def __repr__(self):
        return self.string

    def holds(self,assignment):
        """returns the value of Constraint con evaluated in assignment.

        precondition: all variables are assigned in assignment
        """
        return self.condition(*tuple(assignment[v] for v in self.scope))

class CSP(object):
    """A CSP consists of
    * domains, a dictionary that maps each variable to its domain
    * constraints, a list of constraints
    * variables, a set of variables
    * var_to_const, a variable to set of constraints dictionary
    """
    def __init__(self, domains, constraints, positions={}):
        """domains is a variable:domain dictionary
        constraints is a list of constriants
        """
        self.variables = set(domains)
        self.domains = domains
        self.constraints = constraints
        self.positions = positions
        self.var_to_const = {var:set() for var in self.variables}
        for con in constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)

    def __str__(self):
        """string representation of CSP"""
        return str(self.domains)

    def __repr__(self):
        """more detailed string representation of CSP"""
        return "CSP("+str(self.domains)+", "+str([str(c) for c in self.constraints])+")"

    def consistent(self,assignment):
        """assignment is a variable:value dictionary
        returns True if all of the constraints that can be evaluated
                        evaluate to True given assignment.
        """
        return all(con.holds(assignment)
                    for con in self.constraints
                    if all(v in  assignment  for v in con.scope))
class MapColoringCSP(object):
    """A CSP consists of
    * domains, a dictionary that maps each variable to its domain
    * constraints, a list of constraints
    * variables, a set of variables
    * var_to_const, a variable to set of constraints dictionary
    """
    def __init__(self, colors3,string):
        """domains is a variable:domain dictionary
        constraints is a list of constriants
        """
        self.states=[]
        self.constraints=[]
        neighs=[]
        self.domains={}
        #split string on a ; or :
        import re
        y=re.split('[;:]',string)
        # loop through the string even index is a state the odd is its neighbors
        i=0
        while i< len(y):
            if i%2==0:
                #strip the string containing state name 
                str=y[i].replace(" ","")
                str2=str.replace("\n","")
                #add to state list
                self.states.append(str2)
                #set the domain to the set of colors 
                self.domains[str2]=colors3
            else:
                #access the string of neighboring states 
                countrylist= y[i]
                z=countrylist.split()
                #split this by state and check that each state is in the domain dict we created 
                for state in z:
                    if state not in self.domains:
                        self.domains[state]=colors3
                neighs.append(z)
            i+=1
        i=0
        #check the list of neighbors and the state list to create constraints  
        while i<len(neighs):
            j=0
            while j<len(neighs[i]):
                #add these constrainst to a list
                self.constraints.append(Constraint((self.states[i],neighs[i][j]),ne))
                j+=1
            i+=1
        self.var_to_const = {var:set() for var in self.domains}
        # continue using the methods of csp
        for con in self.constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)
        self.variables=self.domains

    def __str__(self):
        """string representation of CSP"""
        return str(self.domains)

    def __repr__(self):
        """more detailed string representation of CSP"""
        return "CSP("+str(self.domains)+", "+str([str(c) for c in self.constraints])+")"

    def consistent(self,assignment):
        """assignment is a variable:value dictionary
        returns True if all of the constraints that can be evaluated
                        evaluate to True given assignment.
        """
        return all(con.holds(assignment)
                    for con in self.constraints
                    if all(v in  assignment  for v in con.scope))
class NQueensCSP(CSP):
    def __init__(self, n):
        self.domains = {}
        self.constraints = []
        self.positions = {}
        queens=set()
        #create a list of values 0-n
        domainlist= set(range(0,n))
        #set this as domain value for each queen {0:{0,1,2,3}, 1:{0,1,2,3},2:{0,1,2,3},3:{0,1,2,3}}
        for val in range (0, n):
            self.domains[str(val)]=domainlist
            queens.add((val,0))
        #give the constraints 
        for queen in queens:
            for queen2 in queens:
                if queen is not queen2:
                    differenceRow= abs(queen[0]-queen2[0])
                    self.constraints.append(Constraint((str(queen[0]),str(queen2[0])),ne))
                    self.constraints.append(Constraint((str(queen[0]),str(queen2[0])),safeDiagonal(differenceRow)))
             
        self.var_to_const = {var:set() for var in self.domains}
        # continue using the methods of csp
        for con in self.constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)
        self.variables=self.domains


    def __str__(self):
        """string representation of CSP"""
        return str(self.domains)

    def __repr__(self):
        """more detailed string representation of CSP"""
        return "CSP("+str(self.domains)+", "+str([str(c) for c in self.constraints])+")"

    def consistent(self,assignment):
        """assignment is a variable:value dictionary
        returns True if all of the constraints that can be evaluated
                        evaluate to True given assignment.
        """
        return all(con.holds(assignment)
                    for con in self.constraints
                    if all(v in  assignment  for v in con.scope))
        





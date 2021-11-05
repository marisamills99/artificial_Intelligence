from cspExamples import csp1, csp2, csp6, csp5, australia_csp, add_csp2, zebra_puzzle, usa_csp,add_csp, france_csp
from cspProblem import MapColoringCSP, NQueensCSP
from cspConsistency import Search_with_AC_from_CSP,Con_solver
# Test Solving CSPs with Arc consistency and domain splitting:
#1. For Map Coloring problem,
def convert_to_list(solution):
	mylist=[]
	for key in solution:
		tup= (int(key),int(solution[key]))
		mylist.append(tup)
	return mylist
def solveMapColoringCSP(colors:list, neighbors:str):
#returns Dict with state as key and color as value
#Example: {'A': 'R', 'B': 'G', 'C': 'R', 'D': 'G', 'E': 'R', 'F': 'G'}\
    #Con_solver.max_display_level = 0
    colors=set(colors)
    csp = MapColoringCSP(colors,neighbors)
    searcher1d=Con_solver(csp).solve_one()
    # solution = convert_to_dict(searcher1d)
    # print("My solution is----> ")
    # print(solution)
    return searcher1d

#2. For Zebra Puzzles

def solveZebraBasic():
#returns a dictionary with house number as key and list of features as the value
#for example, the solution dictionary for solveZebraBasic() looks like below
#{
#    1: [blue, Norwegian],
#    2: [red, Italian],
#    3: [white, Spanish]
#}]
    #searcher2c = Searcher(Search_with_AC_from_CSP(zebra_puzzle))
    searcher=Con_solver(zebra_puzzle).solve_one()
    #solution = convert_to_dict_as_required(searcher2c.search())
    return searcher

def solveZebraMovieNight():
#returns a dictionary similar to solveZebraBasic
    searcher=Con_solver(csp5).solve_one()
    #solution = convert_to_dict_as_required(searcher2c.search())
    return searcher
def solveZebraEinsteinRiddle():
#returns a dictionary similar to solveZebraBasic
#3. For Cryptarithmetic puzzles,
    searcher=Con_solver(csp6).solve_one()
    #solution = convert_to_dict_as_required(searcher2c.search())
    return searcher

def solveTwoTwoFour():
#returns Dict with character as key and the possible number as value
#Example: {'A': 5, 'B': 7, 'C': 4, 'D': 5, 'E': 7, 'C1':0, 'C2':1, 'C3':0}
    searcher=Con_solver(add_csp).solve_one()
    #solution = convert_to_dict_as_required(searcher2c.search())
    return searcher

def solveSendMoreMoney():
#Example: {'A': 5, 'B': 7, 'C': 4, 'D': 5, 'E': 7, 'C1':0, 'C2':1, 'C3':0}

#4. For Nqueens problem:
    searcher=Con_solver(add_csp2).solve_one()
    #solution = convert_to_dict_as_required(searcher2c.search())
    return searcher

def solveNQueens(n:int):
#returns list of tuples of the coordinates of all the queens.
#Example solution for n=4: [(0,2), (1,0), (2,3), (3, 1)] while the below is how the queens are arranged.
#- - Q -   
#Q - - -   
#- - - Q   
#- Q - -
    csp=NQueensCSP(n)
    searcher1d=Con_solver(csp).solve_one()
    solution = convert_to_list(searcher1d)
    return solution

solveNQueens(8)   
solveMapColoringCSP(list('RGBY'),
                         """WA: OR ID; OR: ID NV CA; CA: NV AZ; NV: ID UT AZ; ID: MT WY UT;
                         UT: WY CO AZ; MT: ND SD WY; WY: SD NE CO; CO: NE KA OK NM; NM: OK TX AZ;
                         ND: MN SD; SD: MN IA NE; NE: IA MO KA; KA: MO OK; OK: MO AR TX;
                         TX: AR LA; MN: WI IA; IA: WI IL MO; MO: IL KY TN AR; AR: MS TN LA;
                         LA: MS; WI: MI IL; IL: IN KY; IN: OH KY; MS: TN AL; AL: TN GA FL;
                         MI: OH IN; OH: PA WV KY; KY: WV VA TN; TN: VA NC GA; GA: NC SC FL;
                         PA: NY NJ DE MD WV; WV: MD VA; VA: MD DC NC; NC: SC; NY: VT MA CT NJ;
                         NJ: DE; DE: MD; MD: DC; VT: NH MA; MA: NH RI CT; CT: RI; ME: NH;
                         HI: ; AK: """)
solveMapColoringCSP(list('RGB'), """SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: """)						 
solveMapColoringCSP(list('RGBY'),
                            """AL: LO FC; AQ: MP LI PC; AU: LI CE BO RA LR MP; BO: CE IF CA FC RA
                            AU; BR: NB PL; CA: IF PI LO FC BO; CE: PL NB NH IF BO AU LI PC; FC: BO
                            CA LO AL RA; IF: NH PI CA BO CE; LI: PC CE AU MP AQ; LO: CA AL FC; LR:
                            MP AU RA PA; MP: AQ LI AU LR; NB: NH CE PL BR; NH: PI IF CE NB; NO:
                            PI; PA: LR RA; PC: PL CE LI AQ; PI: NH NO CA IF; PL: BR NB CE PC; RA:
                            AU BO FC PA LR""")	
solveTwoTwoFour()
solveSendMoreMoney()
solveZebraBasic()
solveZebraMovieNight()
solveZebraEinsteinRiddle()
							
 
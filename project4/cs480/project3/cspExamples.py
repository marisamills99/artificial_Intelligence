# cspExamples.py - Example CSPs
# AIFCA Python3 code Version 0.8.2 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from cspProblem import CSP, Constraint, MapColoringCSP        
from operator import lt,ne,eq,gt

def ne_(val):
    """not equal value"""
    # nev = lambda x: x != val   # alternative definition
    # nev = partial(neq,val)     # another alternative definition
    def nev(x):
        return val != x
    nev.__name__ = str(val)+"!="      # name of the function 
    return nev

def is_(val):
    """is a value"""
    # isv = lambda x: x == val   # alternative definition
    # isv = partial(eq,val)      # another alternative definition
    def isv(x):
        return val == x
    isv.__name__ = str(val)+"=="
    return isv

def addup(a, b, c, d, e):
    #c0 is set to 0 automattically 
    return ((a + b + c) == (d + (e * 10)))

csp0 = CSP({'X':{1,2,3},'Y':{1,2,3}, 'Z':{1,2,3}},
           [ Constraint(('X','Y'),lt),
             Constraint(('Y','Z'),lt)])

C0 = Constraint(('A','B'), lt, "A < B")
C1 = Constraint(('B',), ne_(2), "B != 2")
C2 = Constraint(('B','C'), lt, "B < C")
csp1 = CSP({'A':{1,2,3,4},'B':{1,2,3,4}, 'C':{1,2,3,4}},
           [C0, C1, C2],
           positions={"A": (1, 0),
                      "B": (3, 0),
                      "C": (5, 0),
                      "A < B": (2, 1),
                      "B < C": (4, 1),
                      "B != 2": (3, 2)})

csp2 = CSP({'A':{1,2,3,4},'B':{1,2,3,4}, 'C':{1,2,3,4}, 
            'D':{1,2,3,4}, 'E':{1,2,3,4}},
           [ Constraint(('B',), ne_(3), "B != 3"),
            Constraint(('C',), ne_(2), "C != 2"),
            Constraint(('A','B'), ne, "A != B"),
            Constraint(('B','C'), ne, "A != C"),
            Constraint(('C','D'), lt, "C < D"),
            Constraint(('A','D'), eq, "A = D"),
            Constraint(('A','E'), gt, "A > E"),
            Constraint(('B','E'), gt, "B > E"),
            Constraint(('C','E'), gt, "C > E"),
            Constraint(('D','E'), gt, "D > E"),
            Constraint(('B','D'), ne, "B != D")])

csp3 = CSP({'A':{1,2,3,4},'B':{1,2,3,4}, 'C':{1,2,3,4}, 
            'D':{1,2,3,4}, 'E':{1,2,3,4}},
           [Constraint(('A','B'), ne, "A != B"),
            Constraint(('A','D'), lt, "A < D"),
            Constraint(('A','E'), lambda a,e: (a-e)%2 == 1, "A-E is odd"), # A-E is odd
            Constraint(('B','E'), lt, "B < E"),
            Constraint(('D','C'), lt, "D < C"),
            Constraint(('C','E'), ne, "C != E"),
            Constraint(('D','E'), ne, "D != E")])

def adjacent(x,y):
   """True when x and y are adjacent numbers"""
   return abs(x-y) == 1

csp4 = CSP({'A':{1,2,3,4,5},'B':{1,2,3,4,5}, 'C':{1,2,3,4,5}, 
            'D':{1,2,3,4,5}, 'E':{1,2,3,4,5}},
           [Constraint(('A','B'), adjacent, "adjacent(A,B)"),
            Constraint(('B','C'), adjacent, "adjacent(B,C)"),
            Constraint(('C','D'), adjacent, "adjacent(C,D)"),
            Constraint(('D','E'), adjacent, "adjacent(D,E)"),
            Constraint(('A','C'), ne, "A != C"),
            Constraint(('B','D'), ne, "A != D"),
            Constraint(('C','E'), ne, "C != E")])

def meet_at(p1,p2):
    """returns a function of two words that is true when the words intersect at postions p1, p2.
    The positions are relative to the words; starting at position 0.
    meet_at(p1,p2)(w1,w2) is true if the same letter is at position p1 of word w1 
         and at position p2 of word w2.
    """
    def meets(w1,w2):
        return w1[p1] == w2[p2]
    meets.__name__ = "meet_at("+str(p1)+','+str(p2)+')'
    return meets


crossword1 = CSP({'one_across':{'ant', 'big', 'bus', 'car', 'has'},
                  'one_down':{'book', 'buys', 'hold', 'lane', 'year'},
                  'two_down':{'ginger', 'search', 'symbol', 'syntax'},
                  'three_across':{'book', 'buys', 'hold', 'land', 'year'},
                  'four_across':{'ant', 'big', 'bus', 'car', 'has'}},
                  [Constraint(('one_across','one_down'), meet_at(0,0)),
                   Constraint(('one_across','two_down'), meet_at(2,0)),
                   Constraint(('three_across','two_down'), meet_at(2,2)),
                   Constraint(('three_across','one_down'), meet_at(0,2)),
                   Constraint(('four_across','two_down'), meet_at(0,4))])

words = {'ant', 'big', 'bus', 'car', 'has','book', 'buys', 'hold',
         'lane', 'year', 'ginger', 'search', 'symbol', 'syntax'}
           
def is_word(*letters, words=words):
    """is true if the letters concatenated form a word in words"""
    return "".join(letters) in words

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
  "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
  "z"]

crossword1d = CSP({'p00':letters, 'p10':letters, 'p20':letters, # first row
                   'p01':letters, 'p21':letters,  # second row
                   'p02':letters, 'p12':letters, 'p22':letters, 'p32':letters, # third row
                   'p03':letters, 'p23':letters, #fourth row
                   'p24':letters, 'p34':letters, 'p44':letters, # fifth row
                   'p25':letters # sixth row
                   },
                  [Constraint(('p00', 'p10', 'p20'), is_word), #1-across
                   Constraint(('p00', 'p01', 'p02', 'p03'), is_word), # 1-down
                   Constraint(('p02', 'p12', 'p22', 'p32'), is_word), # 3-across
                   Constraint(('p20', 'p21', 'p22', 'p23', 'p24', 'p25'), is_word), # 2-down
                   Constraint(('p24', 'p34', 'p44'), is_word) # 4-across
                   ])
               
               
colors3={"red","blue","green"}
colors4={"red","yellow","blue","green"}
# Australia: There are 7 states/teritories. Tasmania does not have any neighbors. Three colors suffice.
australia_csp = MapColoringCSP(colors3, """SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: """)

# USA, 4 colors needed.
usa_csp = MapColoringCSP(colors4,
                         """WA: OR ID; OR: ID NV CA; CA: NV AZ; NV: ID UT AZ; ID: MT WY UT;
                         UT: WY CO AZ; MT: ND SD WY; WY: SD NE CO; CO: NE KA OK NM; NM: OK TX AZ;
                         ND: MN SD; SD: MN IA NE; NE: IA MO KA; KA: MO OK; OK: MO AR TX;
                         TX: AR LA; MN: WI IA; IA: WI IL MO; MO: IL KY TN AR; AR: MS TN LA;
                         LA: MS; WI: MI IL; IL: IN KY; IN: OH KY; MS: TN AL; AL: TN GA FL;
                         MI: OH IN; OH: PA WV KY; KY: WV VA TN; TN: VA NC GA; GA: NC SC FL;
                         PA: NY NJ DE MD WV; WV: MD VA; VA: MD DC NC; NC: SC; NY: VT MA CT NJ;
                         NJ: DE; DE: MD; MD: DC; VT: NH MA; MA: NH RI CT; CT: RI; ME: NH;
                         HI: ; AK: """)

zebra_puzzle=CSP({'blue':{1,2,3} ,'red':{1,2,3},'white':{1,2,3},'Italian':{1,2,3},'Norwegian':{1,2,3}, 'Spanish':{1,2,3}},
                 [Constraint(('blue','red'),ne), Constraint(('white','red'),ne),
                             Constraint(('blue','white'),ne), Constraint(('Italian','Norwegian'),ne), 
                        Constraint(('Italian','Spanish'),ne), Constraint(('Norwegian','Spanish'),ne), 
                             Constraint(('Spanish','red'),gt), Constraint(('Italian',),is_(2)),Constraint(('Norwegian','blue'),eq)] )

def toleft(x, y):
    return (y - x) == 1


def toright(x, y):
    return (x - y) == 1


def adjacent(x,y):
    """True when x and y are adjacent numbers"""
    return abs(x-y) == 1
csp5 = CSP({'Black': {1, 2, 3, 4}, 'Blue': {1, 2, 3, 4}, 'Green': {1, 2, 3, 4}, 'Red': {1, 2, 3, 4},
            'Daniel': {1, 2, 3, 4}, 'Joshua': {1, 2, 3, 4}, 'Nicholas': {1, 2, 3, 4}, 'Ryan': {1, 2, 3, 4},
            'Action': {1, 2, 3, 4}, 'Comedy': {1, 2, 3, 4}, 'Horror': {1, 2, 3, 4}, 'Thriller': {1, 2, 3, 4},
            'Chips': {1, 2, 3, 4}, 'Cookies': {1, 2, 3, 4}, 'Crackers': {1, 2, 3, 4}, 'Popcorn': {1, 2, 3, 4},
            '11 years': {1, 2, 3, 4}, '12 years': {1, 2, 3, 4}, '13 years': {1, 2, 3, 4}, '14 years': {1, 2, 3, 4}},
               [ Constraint(('Joshua',), ne_(2), 'Joshua != 2'),
                 Constraint(('Joshua',), ne_(3), 'Joshua != 3'),
                 Constraint(('Black', '11 years'), lt, 'Black < 11'),
                 Constraint(('Joshua', 'Horror'), eq, 'Joshua = Horror'),
                 Constraint(('14 years',), is_(3), '14 year olr = 3'),
                 Constraint(('Red', '13 years'), gt, 'Red > 13'),
                 Constraint(('Red', 'Action'), lt, 'Red < Action'),
                 Constraint(('Daniel', 'Thriller'), eq, 'Daniel = Thriller'),
                 Constraint(('Cookies',), ne_(2), 'Cookies != 2'),
                 Constraint(('Cookies',), ne_(3), 'Cookies != 3'),
                 Constraint(('Black', 'Thriller'), toleft, 'Black to the left of Thriller'),
                 Constraint(('Crackers', 'Comedy'), toright, 'Crackers to the left of Comedy'),
                 Constraint(('Red', 'Popcorn'), gt, 'Red > 13'),
                 Constraint(('Red', 'Nicholas'), lt, 'Red < Action'),
                 Constraint(('Thriller',), ne_(2), 'Joshua != 2'),
                 Constraint(('Thriller',), ne_(3), 'Joshua != 3'),
                 Constraint(('Nicholas', 'Joshua'), gt, 'Red > Nicholas'),
                 Constraint(('Nicholas', 'Daniel'), lt, 'Red < Daniel'),
                 Constraint(('Green',), is_(1), 'Green = 1'),

                 Constraint(('Black', 'Blue'), ne, 'Black != Blue'),
                 Constraint(('Black', 'Green'), ne, 'Black != Green'),
                 Constraint(('Black', 'Red'), ne, 'Black != Red'),
                 Constraint(('Blue', 'Green'), ne, 'Blue != Green'),
                 Constraint(('Blue', 'Red'), ne, 'Blue != Red'),
                 Constraint(('Green', 'Red'), ne, 'Green != Red'),

                 Constraint(('Daniel', 'Joshua'), ne, 'Daniel != Joshua'),
                 Constraint(('Daniel', 'Nicholas'), ne, 'Daniel != Nicholas'),
                 Constraint(('Daniel', 'Ryan'), ne, 'Daniel != Ryan'),
                 Constraint(('Joshua', 'Nicholas'), ne, 'Joshua != Nicholas'),
                 Constraint(('Joshua', 'Ryan'), ne, 'Joshua != Ryan'),
                 Constraint(('Nicholas', 'Ryan'), ne, 'Nicholas != Ryan'),

                 Constraint(('Action', 'Comedy'), ne, 'Action != Comedy'),
                 Constraint(('Action', 'Horror'), ne, 'Action != Horror'),
                 Constraint(('Action', 'Thriller'), ne, 'Action != Thriller'),
                 Constraint(('Comedy', 'Horror'), ne, 'Comedy != Horror'),
                 Constraint(('Comedy', 'Thriller'), ne, 'Comedy != Thriller'),
                 Constraint(('Horror', 'Thriller'), ne, 'Horror != Thriller'),

                 Constraint(('Chips', 'Cookies'), ne, 'Chips != Cookies'),
                 Constraint(('Chips', 'Crackers'), ne, 'Chips != Crackers'),
                 Constraint(('Chips', 'Popcorn'), ne, 'Chips != Popcorn'),
                 Constraint(('Cookies', 'Crackers'), ne, 'Cookies != Crackers'),
                 Constraint(('Cookies', 'Popcorn'), ne, 'Cookies != Popcorn'),
                 Constraint(('Crackers', 'Popcorn'), ne, 'Crackers != Popcorn'),

                 Constraint(('11 years', '12 years'), ne, '11 != 12'),
                 Constraint(('11 years', '13 years'), ne, '11 != 13'),
                 Constraint(('11 years', '14 years'), ne, '11 != 14'),
                 Constraint(('12 years', '13 years'), ne, '12 != 13'),
                 Constraint(('12 years', '14 years'), ne, '12 != 14'),
                 Constraint(('13 years', '14 years'), ne, '13 != 14')
                 ]
               )

csp6 = CSP({'Blue': {1, 2, 3, 4, 5}, 'Green': {1, 2, 3, 4, 5}, 'Red': {1, 2, 3, 4, 5}, 'White': {1, 2, 3, 4, 5}, 'Yellow': {1, 2, 3, 4, 5},
            'Brit': {1, 2, 3, 4, 5}, 'Dane': {1, 2, 3, 4, 5}, 'German': {1, 2, 3, 4, 5}, 'Norwegian': {1, 2, 3, 4, 5}, 'Swede': {1, 2, 3, 4, 5},
            'Beer': {1, 2, 3, 4, 5}, 'Coffee': {1, 2, 3, 4, 5}, 'Milk': {1, 2, 3, 4, 5}, 'Tea': {1, 2, 3, 4, 5}, 'Water': {1, 2, 3, 4, 5},
            'Blends': {1, 2, 3, 4, 5}, 'Blue Master': {1, 2, 3, 4, 5}, 'Dunhill': {1, 2, 3, 4, 5}, 'Pall Mall': {1, 2, 3, 4, 5}, 'Prince': {1, 2, 3, 4, 5},
            'Birds': {1, 2, 3, 4, 5}, 'Cats': {1, 2, 3, 4, 5}, 'Dogs': {1, 2, 3, 4, 5}, 'Horses': {1, 2, 3, 4, 5}, 'Fish': {1, 2, 3, 4, 5}},
                [ Constraint(('Brit', 'Red'), eq, 'Brit = Red'),
                  Constraint(('Swede', 'Dogs'), eq, 'Swede = Dogs'),
                  Constraint(('Dane', 'Tea'), eq, 'Dane = Tea'),
                  Constraint(('Green', 'White'), toleft, 'Green is to the left of white'),
                  Constraint(('Green', 'Coffee'), eq, 'Green = Coffee'),
                  Constraint(('Pall Mall', 'Birds'), eq, 'Pall Mall = Birds'),
                  Constraint(('Yellow', 'Dunhill'), eq, 'Yellow = Dunhill'),
                  Constraint(('Milk',), is_(3), 'Milk = 3'),
                  Constraint(('Norwegian',), is_(1), 'Norwegian = 1'),
                  Constraint(('Blends', 'Cats'), adjacent, 'Blends is adjacent to Cats'),
                  Constraint(('Horses', 'Dunhill'), adjacent, 'Horses is adjacent to Dunhill'),
                  Constraint(('Blue Master', 'Beer'), eq, 'Blue Master = Beer'),
                  Constraint(('German', 'Prince'), eq, 'German = Prince'),
                  Constraint(('Norwegian', 'Blue'), eq, 'Norwegian is equal to Blue'),
                  Constraint(('Blends', 'Water'), adjacent, 'Blends is adjacent to Water'),

                  Constraint(('Blue', 'Green'), ne, 'Blue != Green'),
                  Constraint(('Blue', 'Red'), ne, 'Blue != Red'),
                  Constraint(('Blue', 'White'), ne, 'Blue != White'),
                  Constraint(('Blue', 'Yellow'), ne, 'Blue != Yellow'),
                  Constraint(('Green', 'Red'), ne, 'Green != Red'),
                  Constraint(('Green', 'White'), ne, 'Green != White'),
                  Constraint(('Green', 'Yellow'), ne, 'Green != Yellow'),
                  Constraint(('Red', 'White'), ne, 'Red != White'),
                  Constraint(('Red', 'Yellow'), ne, 'Red != Yellow'),
                  Constraint(('White', 'Yellow'), ne, 'White != Yellow'),

                  Constraint(('Brit', 'Dane'), ne, 'Brit != Dane'),
                  Constraint(('Brit', 'German'), ne, 'Brit != German'),
                  Constraint(('Brit', 'Norwegian'), ne, 'Brit != Norwegian'),
                  Constraint(('Brit', 'Swede'), ne, 'Brit != Swede'),
                  Constraint(('Dane', 'German'), ne, 'Dane != German'),
                  Constraint(('Dane', 'Norwegian'), ne, 'Dane != Norwegian'),
                  Constraint(('Dane', 'Swede'), ne, 'Dane != Swede'),
                  Constraint(('German', 'Norwegian'), ne, 'German != Norwegian'),
                  Constraint(('German', 'Swede'), ne, 'German != Swede'),
                  Constraint(('Norwegian', 'Swede'), ne, 'Norwegian != Swede'),

                  Constraint(('Beer', 'Coffee'), ne, 'Beer != Coffee'),
                  Constraint(('Beer', 'Milk'), ne, 'Beer != Milk'),
                  Constraint(('Beer', 'Tea'), ne, 'Beer != Tea'),
                  Constraint(('Beer', 'Water'), ne, 'Beer != Water'),
                  Constraint(('Coffee', 'Milk'), ne, 'Coffee != Milk'),
                  Constraint(('Coffee', 'Tea'), ne, 'Coffee != Tea'),
                  Constraint(('Coffee', 'Water'), ne, 'Coffee != Water'),
                  Constraint(('Milk', 'Tea'), ne, 'Milk != Tea'),
                  Constraint(('Milk', 'Water'), ne, 'Milk != Water'),
                  Constraint(('Tea', 'Water'), ne, 'Tea != Water'),

                  Constraint(('Blends', 'Blue Master'), ne, 'Blends != Blue Master'),
                  Constraint(('Blends', 'Dunhill'), ne, 'Blends != Dunhill'),
                  Constraint(('Blends', 'Pall Mall'), ne, 'Blends != Pall Mall'),
                  Constraint(('Blends', 'Prince'), ne, 'Blends != Prince'),
                  Constraint(('Blue Master', 'Dunhill'), ne, 'Blue Master != Dunhill'),
                  Constraint(('Blue Master', 'Pall Mall'), ne, 'Blue Master != Pall Mall'),
                  Constraint(('Blue Master', 'Prince'), ne, 'Blue Master != Prince'),
                  Constraint(('Dunhill', 'Pall Mall'), ne, 'Dunhill != Pall Mall'),
                  Constraint(('Dunhill', 'Prince'), ne, 'Dunhill != Prince'),
                  Constraint(('Pall Mall', 'Prince'), ne, 'Pall Mall != Prince'),

                  Constraint(('Birds', 'Cats'), ne, 'Birds != Cats'),
                  Constraint(('Birds', 'Dogs'), ne, 'Birds != Dogs'),
                  Constraint(('Birds', 'Horses'), ne, 'Birds != Horses'),
                  Constraint(('Birds', 'Fish'), ne, 'Birds != Fish'),
                  Constraint(('Cats', 'Dogs'), ne, 'Cats != Dogs'),
                  Constraint(('Cats', 'Horses'), ne, 'Cats != Horses'),
                  Constraint(('Cats', 'Fish'), ne, 'Cats != Fish'),
                  Constraint(('Dogs', 'Horses'), ne, 'Dogs != Horses'),
                  Constraint(('Dogs', 'Fish'), ne, 'Dogs != Fish'),
                  Constraint(('Horses', 'Fish'), ne, 'Horses != Fish')

           ])
# number_puzzle=CSP({'F':{0,1,2,3,4,5,6,7,8,9},'O':{0,1,2,3,4,5,6,7,8,9},
                    # 'U':{0,1,2,3,4,5,6,7,8,9},'R':{0,1,2,3,4,5,6,7,8,9},
                    # 'T':{0,1,2,3,4,5,6,7,8,9}, 'W':{0,1,2,3,4,5,6,7,8,9},
                    # 'C1':{0,1},'C2':{0,1},'C3':{0,1}},
                 # [Constraint(('O'+'O','R'+10*'C1'),eq), Constraint(('C1'+'W'+'W','U'+ 10*'C2'),eq),
                             # Constraint(('C2'+'T'+'T','O'+10*'C3'),eq), Constraint(('C3','F'),eq)] )
# France, 4 colors needed.
france_csp = MapColoringCSP(list('RGBY'),
                            """AL: LO FC; AQ: MP LI PC; AU: LI CE BO RA LR MP; BO: CE IF CA FC RA
                            AU; BR: NB PL; CA: IF PI LO FC BO; CE: PL NB NH IF BO AU LI PC; FC: BO
                            CA LO AL RA; IF: NH PI CA BO CE; LI: PC CE AU MP AQ; LO: CA AL FC; LR:
                            MP AU RA PA; MP: AQ LI AU LR; NB: NH CE PL BR; NH: PI IF CE NB; NO:
                            PI; PA: LR RA; PC: PL CE LI AQ; PI: NH NO CA IF; PL: BR NB CE PC; RA:
                            AU BO FC PA LR""")
add_csp = CSP({'F':{1,2,3,4,5,6,7,8,9},'O':{0,1,2,3,4,5,6,7,8,9},
                    'U':{0,1,2,3,4,5,6,7,8,9},'R':{0,1,2,3,4,5,6,7,8,9},
                    'T':{0,1,2,3,4,5,6,7,8,9}, 'W':{0,1,2,3,4,5,6,7,8,9},
                    'C0':{0}, 'C1':{0,1},'C2':{0,1},'C3':{0,1}},
                 [Constraint(('C0', 'O', 'O', 'R', 'C1'), addup),
                  Constraint(('C1', 'W', 'W', 'U', 'C2'), addup),
                  Constraint(('C2', 'T', 'T', 'O', 'C3'), addup),
                  Constraint(('C3', 'F'), eq),
                  Constraint(('F', 'O'), ne),
                  Constraint(('F', 'U'), ne),
                  Constraint(('F', 'R'), ne),
                  Constraint(('F', 'T'), ne),
                  Constraint(('F', 'W'), ne),
                  Constraint(('O', 'U'), ne),
                  Constraint(('O', 'R'), ne),
                  Constraint(('O', 'T'), ne),
                  Constraint(('O', 'W'), ne),
                  Constraint(('U', 'R'), ne),
                  Constraint(('U', 'T'), ne),
                  Constraint(('U', 'W'), ne),
                  Constraint(('T', 'W'), ne),
                  ])

add_csp2 = CSP({'S':{0,1,2,3,4,5,6,7,8,9},'E':{0,1,2,3,4,5,6,7,8,9},
                    'N':{0,1,2,3,4,5,6,7,8,9},'D':{0,1,2,3,4,5,6,7,8,9},
                    'M':{0,1,2,3,4,5,6,7,8,9}, 'O':{0,1,2,3,4,5,6,7,8,9},
                    'R':{0,1,2,3,4,5,6,7,8,9}, 'Y':{0,1,2,3,4,5,6,7,8,9},
                    'C0':{0}, 'C1':{0,1},'C2':{0,1},'C3':{0,1}, 'C4':{0,1}},
                 [Constraint(('C0', 'D', 'E', 'Y', 'C1'), addup),
                  Constraint(('C1', 'N', 'R', 'E', 'C2'), addup),
                  Constraint(('C2', 'E', 'O', 'N', 'C3'), addup),
                  Constraint(('C3', 'S', 'M', 'O', 'C3'), addup),
                  Constraint(('C4', 'M'), eq),
                  Constraint(('S', 'E'), ne),
                  Constraint(('S', 'N'), ne),
                  Constraint(('S', 'D'), ne),
                  Constraint(('S', 'M'), ne),
                  Constraint(('S', 'O'), ne),
                  Constraint(('S', 'R'), ne),
                  Constraint(('S', 'Y'), ne),
                  Constraint(('E', 'N'), ne),
                  Constraint(('E', 'D'), ne),
                  Constraint(('E', 'M'), ne),
                  Constraint(('E', 'O'), ne),
                  Constraint(('E', 'R'), ne),
                  Constraint(('E', 'Y'), ne),
                  Constraint(('N', 'D'), ne),
                  Constraint(('N', 'M'), ne),
                  Constraint(('N', 'O'), ne),
                  Constraint(('N', 'R'), ne),
                  Constraint(('N', 'Y'), ne),
                  Constraint(('D', 'N'), ne),
                  Constraint(('D', 'O'), ne),
                  Constraint(('D', 'R'), ne),
                  Constraint(('D', 'Y'), ne),
                  Constraint(('M', 'O'), ne),
                  Constraint(('M', 'R'), ne),
                  Constraint(('M', 'Y'), ne),
                  Constraint(('O', 'R'), ne),
                  Constraint(('O', 'Y'), ne),
                  Constraint(('R', 'Y'), ne),
                  ])
    
def test(CSP_solver, csp=csp1,
             solutions=[{'A': 1, 'B': 3, 'C': 4}, {'A': 2, 'B': 3, 'C': 4}]):
    """CSP_solver is a solver that takes a csp and returns a solution
    csp is a constraint satisfaction problem
    solutions is the list of all solutions to csp
    This tests whether the solution returned by CSP_solver is a solution.
    """
    print("Testing csp with",CSP_solver.__doc__)
    sol0 = CSP_solver(csp)
    print("Solution is found:",sol0)
    assert sol0 in solutions, "Solution not correct for "+str(csp)
    print("Passed unit test")


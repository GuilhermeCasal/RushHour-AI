
from common import Map
from methods import Ia
from tree_search import SearchProblem, SearchTree


f = open("levels.txt", "r")

for i,x in enumerate(f):
    if int(x.split(" ")[0]) > 5 and int(x.split(" ")[0]) < 12 or int(x.split(" ")[0]) > 25: continue
    state = {"dimensions": [6, 6], "level": 1, "grid": x, "score": -1, "game_speed": 10, "cursor": [3, 3], "selected": ""}
    
    estado = str(state["grid"])
    est = estado.split("\n")
    # estado = Map(est[0])
    alg = Ia([3,3])
    # # p = SearchProblem(alg, coord) 
    print(est[0])   
    p = SearchProblem(alg, est[0])  
    t = SearchTree(p) 
    k = t.search()
    # print(k)
    # print("len",k)

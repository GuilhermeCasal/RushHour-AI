
from abc import ABC, abstractmethod

class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial):
        self.domain = domain    # domain methods
        self.initial = initial
    def goal_test(self, grid, goal):
        return self.domain.satisfies(grid,goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent, action, cost =0, heuristic = 0, xlist = [], ylist = []):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.action = action

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, goal = None):
        self.problem = problem  # recebe um objeto SearchProblem
        root = SearchNode(problem.initial, None, None)
        self.open_nodes = [root]    # estado da grid
        self.ext_nodes = [root.state]
        self.goal = goal

    # procurar a solucao
    def search(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)        
            if self.problem.goal_test(node.state,self.goal):
                lis = []
                cost = 0
                while node != None:
                    lis = [node] + lis
                    cost = cost + node.cost
                    node = node.parent
                return lis
            lnewnodes = []
            for action in self.problem.domain.actions():
                i = 1
                while i < len(action):
                    nova_grid = self.problem.domain.result(action[0],action[i],node.state)
                    if nova_grid not in self.ext_nodes:
                        newnode = SearchNode(
                            nova_grid,
                            node,
                            action= [action[0]] + [action[i]],
                            cost = node.cost + self.problem.domain.cost(action[0],node.action),
                            heuristic = self.problem.domain.heuristic(action[0])
                        )
                        lnewnodes.append(newnode)
                        self.ext_nodes += [nova_grid]
                    i = i + 1
            self.add_to_open(lnewnodes)
        return None

    def add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key= lambda e : e.heuristic + e.cost)
        


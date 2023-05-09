from tree_search import SearchDomain
from common import Coordinates, Map

class Ia(SearchDomain):
    def __init__(self, cursor):
        self.ops = None
        self.letters = []
        self.xlist = []
        self.xlist = []

    def actions(self): 
        moves = [Coordinates(0,1), Coordinates(0,-1), Coordinates(1,0), Coordinates(-1,0)]
        self.letters = self.get_letters(self.ops.grid)
        self.xlist, self.ylist = self.get_all_coords(self.letters)
        actlist = []    # vai ser retornado com o conjunto de todas as coordenadas onde self se pode deslocar
        value =  []
        grid_size = len(self.ops.grid)-1

        for i,piece in enumerate(self.letters):
            place = self.xlist[i]
            if piece != "x":
                if place[0].y == place[1].y:    # return True se a peça estiver na horizontal ou false se estiver na vertical ([4,3] [5,3])
                    orientacao = True
                else:
                    orientacao = False
                placeLength = len(place)
                
                if orientacao:
                    boo = True
                    boo_2 = True
                    for c in self.ylist:
                        if boo:
                            if place[0].x <= 0 or Coordinates(place[0].x-1,place[0].y) == c:
                                boo = False
                        if boo_2:
                            if place[placeLength-1].x >= grid_size or Coordinates(place[placeLength-1].x+1,place[placeLength-1].y) == c:
                                boo_2 = False
                    if boo:
                        actlist.append(moves[3])
                    if boo_2:
                        actlist.append(moves[2])
                else:
                    boo = True
                    boo_2 = True
                    for c in self.ylist:
                        if boo_2:
                            if place[0].y <= 0 or Coordinates(place[0].x,place[0].y-1) == c:
                                boo_2 = False
                        if boo:
                            if place[placeLength-1].y >= grid_size or Coordinates(place[placeLength-1].x,place[placeLength-1].y+1) == c:
                                boo = False
                    if boo:
                        actlist.append(moves[0])
                    if boo_2:
                        actlist.append(moves[1])
            value += [[piece] + actlist]
            actlist = []
        return value

    def result(self,piece,action,state):
        newstate = Map(state)
        newstate.move(piece, action)
        str_grid = "0" + newstate.__repr__()  
        return str_grid

    def cost(self, piece, prev_piece):
        # if len(self.ops.grid)-1 <= 6 and prev_piece != None and piece != prev_piece[0]:
        #     return 1
        return 0
        # index = self.letters.index(piece)
        # piece_coord = self.xlist[index] #self.ops.piece_coordinates(piece)
        
        # if prev_piece == None:
        #     return (int)(math.sqrt((self.cursor[0] - piece_coord[0].x)**2 + (self.cursor[1] - piece_coord[0].y)**2))
        # # prev_coord = self.ops.piece_coordinates(prev_piece[0])
        # index = self.letters.index(prev_piece[0])
        # prev_coord = self.xlist[index]
        # return (int)(math.sqrt((prev_coord[0].x - piece_coord[0].x)**2 + (prev_coord[0].y - piece_coord[0].y)**2))

    def heuristic(self,piece): 
        index = self.letters.index("A")
        car_coord = self.xlist[index]
        i = 0
        j = 0
        index = self.letters.index(piece)

        grid_size = len(self.ops.grid)-1
        for k in self.xlist:
            while j < len(k):
                if k[j].y == car_coord[1].y and k[j].x > car_coord[1].x:
                    i += 1
                j += 1
            j = 0

        k = grid_size - car_coord[1].x 
        i = i + k
        return i

    def satisfies(self, grid, goal):
        self.ops = Map(grid)
        
        if goal == None:
            return self.ops.test_win()
        else:
            # print(goal)
            if grid == goal:
                print("found")
                return True
        return False

    def get_all_coords(self,letters):
        xlist = []
        ylist = []
        for i in letters:
            coord = self.ops.piece_coordinates(i)
            xlist += [coord]
            ylist += coord
        return xlist, ylist

    def get_letters(self, grid):
        letras = ["A"]

        for line in grid:
            for letter in line:
                if letter == "o":
                    continue
                if letter not in letras:
                    letras = letras + [letter]
        return letras
"""Common data structures. Can be used by any module."""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Coordinates:
    """Coordinates data class."""

    x: int
    y: int


class MapException(Exception):
    """Exception Moving Pieces."""


class Map:
    """Representation of a map."""

    empty_tile = "o"
    wall_tile = "x"
    player_car = "A"

    def __init__(self, txt: str):
        """Initialize Map from string."""
        pieces, grid, movements = txt.split(" ") # "1 ooooooooooooAAoooooooooooooooooooooo 5"
        self.pieces = int(pieces) # 1
        self.movements = int(movements) # 5
        self.grid_size = int(math.sqrt(len(grid))) # ooooooooooooAAoooooooooooooooooooooo
        self.grid = []

        line = []
        #este ciclo for serve para dividir o tabuleiro num array em que cada posição contem o conteudo de uma linha
        for i, pos in enumerate(grid): # i = 0, 1, 2.... // pos = grid[0], grid[1].... (aka oooooo, ooAAoo, ...)
            line.append(pos)
            if (i + 1) % self.grid_size == 0: 
                self.grid.append(line)
                line = []

    def __repr__(self):
        """Revert map object to string."""
        raw = ""
        for line in self.grid:
            for column in line:
                raw += column
        return f"{self.pieces} {raw} {self.movements}"

    @property
    def coordinates(self):  # envia um elemento que imprime x,y e letra pela ordem que aparece na string, logo 
                            # a mesma letra pode estar em posições separadas da grid se estiver na vertical
                            # [(2, 1, 'B'), (0, 2, 'A'), (1, 2, 'A'), (2, 2, 'B')] de notar que não é uma lista, só um elemento
                            # como dá para ver pelos []
        """Representation of ocupied map positions through tuples x,y,value."""
        _coordinates = []

        for y, line in enumerate(self.grid):
            for x, column in enumerate(line):
                if column != self.empty_tile:
                    _coordinates.append((x, y, column))

        return _coordinates

    def get(self, cursor: Coordinates):     # imprime a letra em que o cursor está
        """Return piece at cursor position."""
        if 0 <= cursor.x < self.grid_size and 0 <= cursor.y < self.grid_size:
            return self.grid[int(cursor.y)][int(cursor.x)]
        raise MapException("Out of the grid")

    def piece_coordinates(self, piece: str):
        """List coordinates holding a piece."""
        return [Coordinates(x, y) for (x, y, p) in self.coordinates if p == piece]

#   ENVIAR (1,0) É ADICIONAR 1 AO x O QUE MOVE A PEÇA NA VERTICAL
    # (0,1) FAZ O MESMO PARA y (HORIZONTAL)
    def move(self, piece: str, direction: Coordinates): # supostamente cria uma imagem do tabuleiro
        """Move piece in direction fiven by a vector.""" # com um movimento a mais para o computador analisar o efeito
        if piece == self.wall_tile:                 # sem o custo do tempo de fazer mesmo o movimento
            raise MapException("Blocked piece")     # pode ser usado recursivamente

        piece_coord = self.piece_coordinates(piece)
        # Don't move vertical pieces sideways
        if direction.x != 0 and any([line.count(piece) == 1 for line in self.grid]):
            raise MapException("Can't move sideways")
        # Don't move horizontal pieces up-down
        if direction.y != 0 and any([line.count(piece) > 1 for line in self.grid]):
            raise MapException("Can't move up-down")

        def sum(a: Coordinates, b: Coordinates):
            return Coordinates(a.x + b.x, a.y + b.y)

        for pos in piece_coord:
            if not self.get(sum(pos, direction)) in [piece, self.empty_tile]:
                raise MapException("Blocked piece")

        for pos in piece_coord:
            self.grid[pos.y][pos.x] = self.empty_tile

        for pos in piece_coord:
            new_pos = sum(pos, direction)
            self.grid[new_pos.y][new_pos.x] = piece

    def test_win(self):
        """Test if player_car has crossed the left most column."""
        return any(     # VER A DEFINIÇÃO DE 'ANY' PARA ENTENDER
            [c.x == self.grid_size - 1 for c in self.piece_coordinates(self.player_car)] 
        )


""" TODO move to tests
m = Map("02 ooooBoooooBoAAooBooooooooooooooooooo 14")
print(m)
print(m.get(Dimensions(4,0)))
assert m.move("A", Coordinates(1, 0))
assert m.move("A", Coordinates(-1, 0))
assert not m.move("A", Coordinates(0, 1))
assert not m.move("A", Coordinates(0, -1))
assert m.move("B", Coordinates(0, 1))
assert m.move("B", Coordinates(0, -1))
assert not m.move("B", Coordinates(1,0))
assert not m.move("B", Coordinates(-1,0))
print(m)
"""

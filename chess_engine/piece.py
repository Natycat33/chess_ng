# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 13:33:57 2021

@author: Korean_Crimson
"""
from typing import List
from typing import Tuple

from chess_engine import move
from chess_engine.consts import BISHOP
from chess_engine.consts import KING
from chess_engine.consts import KNIGHT
from chess_engine.consts import PAWN
from chess_engine.consts import QUEEN
from chess_engine.consts import ROOK
from chess_engine.util import convert
from chess_engine.util import convert_str

class Piece:
    """Piece class. Needs to be subclassed by the various chess pieces"""

    def __init__(self, moves, position, representation):
        self.moves = moves
        self.position = convert_str(position) if isinstance(position, str) else position
        self.representation = representation
        self.team = representation[-1]
        self.captured = False
        self.position_history = []
        self._valid_moves = {} #cached moves per board position

    def __repr__(self):
        return f'{self.__class__.__name__}({convert(self.position)})'

    def compute_valid_moves(self, board) -> List[Tuple[int, int]]:
        """Returns a list of squares that the piece can move to or capture at"""
        if board in self._valid_moves:
            return self._valid_moves[board]

        valid_squares = []
        for move_ in self.moves:
            valid_squares_ = move_.compute_valid_moves(board, self)
            valid_squares.extend(valid_squares_)
        return list(set(valid_squares))

    def move_to(self, position, log=True) -> None:
        """Moves the piece to the specified position and adds it to the position history"""
        pos_old = convert(self.position)
        self.position = position
        self.position_history.append(position)
        if log:
            print(f'{self.team}: {self.representation} from {pos_old} to {convert(position)}')

    def can_move_to(self, board, position) -> bool:
        """Returns true if this piece can move to the specified position"""
        return position in self.compute_valid_moves(board)

class Pawn(Piece):
    """Pawn class. Contains all the pawn moves"""

    def __init__(self, direction, position, representation):
        moves = [move.InitialPawnMove(direction),
                 move.PawnMove(direction),
                 move.PawnCapture(direction)]
        super().__init__(moves, position, representation)

class Knight(Piece):
    """Knight class. Contains all the knight moves"""

    def __init__(self, _, position, representation):
        moves = [move.KnightMove()]
        super().__init__(moves, position, representation)

class Bishop(Piece):
    """Bishop class. Contains all the bishop moves"""

    def __init__(self, _, position, representation):
        moves = [move.BishopMove(8)]
        super().__init__(moves, position, representation)

class Rook(Piece):
    """Rook class. Contains all the rook moves"""

    def __init__(self, _, position, representation):
        moves = [move.RookMove()]
        super().__init__(moves, position, representation)

class Queen(Piece):
    """Queen class. Contains all the queen moves"""

    def __init__(self, _, position, representation):
        moves = [move.RookMove(), move.BishopMove(8)]
        super().__init__(moves, position, representation)

class King(Piece):
    """King class. Contains all the king moves"""

    def __init__(self, _, position, representation):
        moves = [move.KingMove()]
        super().__init__(moves, position, representation)

PIECES = {PAWN: Pawn,
          KNIGHT: Knight,
          BISHOP: Bishop,
          ROOK: Rook,
          QUEEN: Queen,
          KING: King}

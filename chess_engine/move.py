# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 12:56:04 2021

@author: Korean_Crimson
"""
import itertools
from dataclasses import dataclass
from typing import List
from typing import Tuple

# pylint: disable=invalid-name
@dataclass
class LineMove:
    """Move class. Encapsulates how a piece moves. To be inherited from when implementing a move"""

    range_: int
    direction: int = 1
    forward_only: bool = False
    horz_move: bool = False
    can_capture: bool = False

    def compute_valid_moves(self, board, piece) -> List[Tuple[int, int]]:
        """Computes all valid moves that can be made from the passed position"""
        x, y = piece.position
        horz_moves = self._compute_horz_moves(x, y, board, piece.team)
        vert_moves = self._compute_vert_moves(x, y, board, piece.team)
        return horz_moves + vert_moves

    def _compute_horz_moves(self, current_x, y, board, team):
        if not self.horz_move:
            return []

        moves = []

        #forward
        for x in range(current_x + 1, board.size):
            square = board[x, y]
            if square is None or square.team != team:
                moves.append((x, y))
            if square is not None:
                break

        #backward
        for x in range(current_x - 1, -1, -1):
            square = board[x, y]
            if square is None or square.team != team:
                moves.append((x, y))
            if square is not None:
                break

        return moves

    def _compute_vert_moves(self, x, current_y, board, team):
        forward_moves = []
        for y in range(current_y - 1, current_y - 1 - self.range_, -1):
            if y < 0:
                break

            square = board[x, y]
            if square is None or (square.team != team and self.can_capture):
                forward_moves.append((x, y))
            if square is not None:
                break

        backward_moves = []
        for y in range(current_y + 1, current_y + 1 + self.range_):
            if y >= board.size:
                break

            square = board[x, y]
            if square is None or (square.team != team and self.can_capture):
                backward_moves.append((x, y))
            if square is not None:
                break

        if self.forward_only:
            return forward_moves if self.direction == -1 else backward_moves
        return forward_moves + backward_moves

# pylint: disable=too-few-public-methods
class BishopMove:
    """Moves diagonally to either side of the board, backwards and forwards"""

    @staticmethod
    def compute_valid_moves(board, piece) -> List[Tuple[int, int]]:
        """Computes all valid moves that can be made from the passed position"""
        moves = []
        x, y = piece.position
        team = piece.team
        for x_dir, y_dir in itertools.product((1, -1), repeat=2):
            pos = (x + x_dir, y + y_dir)
            while board.is_on_board(pos):
                square = board[pos]
                if square is None or square.team != team:
                    moves.append(pos)
                if square is not None:
                    break
                pos = (pos[0] + x_dir, pos[1] + y_dir)
        return moves

class InitialPawnMove(LineMove):
    """Moves 2 spaces forward"""

    def __init__(self, direction):
        range_ = 2
        super().__init__(
            range_, direction, forward_only=True, can_capture=False
        )

    def compute_valid_moves(self, board, piece) -> List[Tuple[int, int]]:
        if len(piece.position_history):
            return []
        return super().compute_valid_moves(board, piece)

class KingMove:
    """Moves 1 space in any direction"""

    @staticmethod
    def compute_valid_moves(board, piece) -> List[Tuple[int, int]]:
        """Computes all valid moves that can be made from the passed position"""
        neighbours = lambda x: [y for y in (x - 1, x, x + 1) if 0 <= y < board.size]
        x, y = piece.position
        return [pos for pos in itertools.product(neighbours(x), neighbours(y))
                if pos != piece.position
                and (board[pos] is None or board[pos].team != piece.team)]

class PawnMove(LineMove):
    """Moves 1 space forward"""

    def __init__(self, direction):
        range_ = 1
        super().__init__(
            range_, direction, forward_only=True, can_capture=False
        )


class PawnCapture:
    """Moves 1 space forward diagonally and needs to capture"""

    def __init__(self, direction):
        self.direction = direction

    def compute_valid_moves(self, board, piece) -> List[Tuple[int, int]]:
        """Computes all valid moves that can be made from the passed position"""
        x, y = piece.position
        moves = ((x + 1, y + self.direction), (x - 1, y + self.direction))
        return [x for x in filter(board.is_on_board, moves)
                if not board.is_empty_at(x) and board.is_enemy(x, piece.team)]

class EnPassantMove:
    """Pawn capture but with a pawn that already passed"""


class RookMove(LineMove):
    """Moves horizontally or vertically for up to 8 spaces"""

    def __init__(self):
        range_ = 8
        super().__init__(range_, horz_move=True, can_capture=True)


class KnightMove:
    """Knight move"""

    INDICES = [(x, y) for x, y in itertools.product((1, 2, -1, -2), repeat=2)
                   if abs(x) != abs(y)]

    @classmethod
    def compute_valid_moves(cls, board, piece) -> List[Tuple[int, int]]:
        """Computes all valid moves that can be made from the passed position"""
        x1, y1 = piece.position
        positions = [(x1 + x2, y1 + y2) for x2, y2 in cls.INDICES]
        return [pos for pos in positions if board.is_on_board(pos)
                and (board.is_empty_at(pos) or board.is_enemy(pos, piece.team))]

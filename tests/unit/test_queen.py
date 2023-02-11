# -*- coding: utf-8 -*-
# type: ignore
"""
Created on Sun Jan  2 23:02:59 2022

@author: richa
"""
import pytest

from chess_ng.board import Board
from chess_ng.piece import Pawn, Queen
from chess_ng.util import convert, convert_str


#pylint: disable=missing-function-docstring
@pytest.mark.parametrize(
    "position,expected",
    [
        ("a1", 7),
        ("b2", 7 + 2),
        ("b1", 6 + 1),
        ("c3", 7 + 4),
        ("c4", 6 + 5),
        ("d4", 7 + 6),
        ("c5", 7 + 4),
        ("c6", 7 + 4),
    ],
)
def test_queen(position, expected):
    piece = Queen(None, convert_str(position), representation="Q1")
    board = Board(pieces=[piece], size=8)
    moves = piece.compute_valid_moves(board)
    assert len(moves) == expected + 14  # bishop + rook moves


@pytest.mark.parametrize(
    "position", ["a1", "a2", "a3", "b3", "c3", "c2", "c1", "b1", "b2"]
)
def test_queen_capture(position):
    piece = Queen(None, convert_str("b2"), representation="Q1")
    piece2 = Pawn(direction=1, position=convert_str(position), representation="o2")
    board = Board(pieces=[piece, piece2], size=8)
    moves = piece.compute_valid_moves(board)
    positions = list(move.position for move in moves)

    if convert_str(position) == piece.position:
        assert convert_str(position) not in positions
    else:
        assert convert_str(position) in positions


@pytest.mark.parametrize(
    "team,expected_moves",
    [
        (2, {"a1", "a2", "a3", "b3", "c3", "c2", "c1", "b1"}),
        (1, set()),
    ],
)
def test_queen_move_not_going_through_targets(team, expected_moves):
    queen = Queen(None, convert_str("b2"), representation="Q1")
    positions = ["a1", "a2", "a3", "b3", "c3", "c2", "c1", "b1"]
    pawns = [
        Pawn(direction=1, position=convert_str(pos), representation=f"o{team}")
        for pos in positions
    ]
    board = Board(pieces=[queen, *pawns], size=8)
    print(board)

    moves = queen.compute_valid_moves(board)
    positions = list(move.position for move in moves)
    assert set(map(convert, positions)) == expected_moves

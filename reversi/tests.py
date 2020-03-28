from __future__ import absolute_import
import unittest
from .reversi import Board

board = Board()


class LegalMoves(unittest.TestCase):
    def test_north_simple(self):
        p1 = sum(board.positions[x] for x in [(5,3)])
        p2 = sum(board.positions[x] for x in [(2,3), (3,3), (4,3)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [(1,3)])

    def test_west_simple(self):
        p1 = sum(board.positions[x] for x in [(3,2)])
        p2 = sum(board.positions[x] for x in [(3,3), (3,4), (3,5)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [(3,6)])

    def test_south_simple(self):
        p1 = sum(board.positions[x] for x in [(2,5)])
        p2 = sum(board.positions[x] for x in [(3,5), (4,5), (5,5)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [(6,5)])

    def test_east_simple(self):
        p1 = sum(board.positions[x] for x in [(4,6)])
        p2 = sum(board.positions[x] for x in [(4,3), (4,4), (4,5)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [(4,2)])

    def test_northeast_simple(self):
        p1 = sum(board.positions[x] for x in [(5,5)])
        p2 = sum(board.positions[x] for x in [(2,2), (3,3), (4,4)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [(1,1)])

    def test_northwest_simple(self):
        p1 = sum(board.positions[x] for x in [(5,2)])
        p2 = sum(board.positions[x] for x in [(4,3), (3,4), (2,5)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [(1,6)])

    def test_southwest_simple(self):
        p1 = sum(board.positions[x] for x in [(2,2)])
        p2 = sum(board.positions[x] for x in [(3,3), (4,4), (5,5)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [(6,6)])

    def test_southeast_simple(self):
        p1 = sum(board.positions[x] for x in [(2,5)])
        p2 = sum(board.positions[x] for x in [(3,4), (4,3), (5,2)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [(6,1)])

    def test_no_simple_west_wraps(self):
        p1 = sum(board.positions[x] for x in [(3,7)])
        p2 = sum(board.positions[x] for x in [(4,0), (4,1)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [])

    def test_no_simple_east_wraps(self):
        p1 = sum(board.positions[x] for x in [(4,0)])
        p2 = sum(board.positions[x] for x in [(3,6), (3,7)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [])

    def test_no_simple_northeast_wraps(self):
        p1 = sum(board.positions[x] for x in [(4,0)])
        p2 = sum(board.positions[x] for x in [(1,6), (2,7)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [])

    def test_no_simple_northwest_wraps(self):
        p1 = sum(board.positions[x] for x in [(3,7)])
        p2 = sum(board.positions[x] for x in [(3,0), (2,1)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [])

    def test_no_simple_southwest_wraps(self):
        p1 = sum(board.positions[x] for x in [(3,7)])
        p2 = sum(board.positions[x] for x in [(5,0), (6,1)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [])

    def test_no_simple_southeast_wraps(self):
        p1 = sum(board.positions[x] for x in [(4,0)])
        p2 = sum(board.positions[x] for x in [(3,6), (4,7)])
        self.assertEqual(board.legal_actions((p1, p2, 2, 1)), [])

    def test_unknown_problem(self):
        p1 = sum(board.positions[x] for x in
                 [(0,4), (1,1), (1,2), (1,3), (1,4), (1,5), (2,1), (2,2),
                  (2,3), (2,4), (2,5), (2,6), (3,1), (3,2), (3,3), (3,4),
                  (3,5), (3,6), (4,0), (4,4), (4,6), (4,7), (5,5), (5,6),
                  (6,4), (6,5), (6,6), (7,5), (7,7)])
        p2 = sum(board.positions[x] for x in
                 [(0,5), (2,0), (2,7), (4,2), (4,3), (4,5), (5,2), (5,4),
                  (6,1), (6,2), (6,3), (7,0), (7,2)])
        self.assertEqual(set(board.legal_actions((p1, p2, 1, 2))),
                         set([(0,1), (0,2), (0,3), (0,6), (1,0), (1,6),
                              (4,1), (5,7), (6,7), (7,4), (7,6)]))


class Plays(unittest.TestCase):
    def test_simple_north_capture(self):
        p1 = sum(board.positions[x] for x in [(5,3)])
        p2 = sum(board.positions[x] for x in [(2,3), (3,3), (4,3)])
        p1_new = p1 | p2 | board.positions[(1,3)]
        self.assertEqual(board.next_state([(p1, p2, 2, 1)], (1, 3)),
                         (p1_new, 0, 1, 1))

    def test_simple_west_capture(self):
        p1 = sum(board.positions[x] for x in [(3,2)])
        p2 = sum(board.positions[x] for x in [(3,3), (3,4), (3,5)])
        p1_new = p1 | p2 | board.positions[(3,6)]
        self.assertEqual(board.next_state([(p1, p2, 2, 1)], (3, 6)),
                         (p1_new, 0, 1, 1))

    def test_simple_south_capture(self):
        p1 = sum(board.positions[x] for x in [(5,3)])
        p2 = sum(board.positions[x] for x in [(2,3), (3,3), (4,3)])
        p1_new = p1 | p2 | board.positions[(1,3)]
        self.assertEqual(board.next_state([(p1, p2, 2, 1)], (1, 3)),
                         (p1_new, 0, 1, 1))

    def test_simple_east_capture(self):
        p1 = sum(board.positions[x] for x in [(2,5)])
        p2 = sum(board.positions[x] for x in [(3,5), (4,5), (5,5)])
        p1_new = p1 | p2 | board.positions[(6,5)]
        self.assertEqual(board.next_state([(p1, p2, 2, 1)], (6, 5)),
                         (p1_new, 0, 1, 1))

    def test_simple_northeast_capture(self):
        p1 = sum(board.positions[x] for x in [(5,5)])
        p2 = sum(board.positions[x] for x in [(2,2), (3,3), (4,4)])
        p1_new = p1 | p2 | board.positions[(1,1)]
        self.assertEqual(board.next_state([(p1, p2, 2, 1)], (1, 1)),
                         (p1_new, 0, 1, 1))

    def test_simple_northwest_capture(self):
        p1 = sum(board.positions[x] for x in [(5,2)])
        p2 = sum(board.positions[x] for x in [(4,3), (3,4), (2,5)])
        p1_new = p1 | p2 | board.positions[(1,6)]
        self.assertEqual(board.next_state([(p1, p2, 2, 1)], (1, 6)),
                         (p1_new, 0, 1, 1))

    def test_simple_southwest_capture(self):
        p1 = sum(board.positions[x] for x in [(2,2)])
        p2 = sum(board.positions[x] for x in [(3,3), (4,4), (5,5)])
        p1_new = p1 | p2 | board.positions[(6,6)]
        self.assertEqual(board.next_state([(p1, p2, 2, 1)], (6, 6)),
                         (p1_new, 0, 1, 1))

    def test_simple_southeast_capture(self):
        p1 = sum(board.positions[x] for x in [(2,5)])
        p2 = sum(board.positions[x] for x in [(3,4), (4,3), (5,2)])
        p1_new = p1 | p2 | board.positions[(6,1)]
        self.assertEqual(board.next_state([(p1, p2, 2, 1)], (6, 1)),
                         (p1_new, 0, 1, 1))

    def test_no_north_wrapped_capture(self):
        p1 = sum(board.positions[x] for x in [(3,4)])
        p2 = sum(board.positions[x] for x in [(1,4), (2,4)])

        x1 = board.positions[(6,3)]
        x2 = board.positions[(7,3)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(0, 4)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (0, 4)),
                         (p1 | p2 | x1 | board.positions[(0,4)], x2, 1, 2))

        x1 = board.positions[(6,4)]
        x2 = board.positions[(7,4)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(0, 4)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (0, 4)),
                         (p1 | p2 | x1 | board.positions[(0,4)], x2, 1, 2))

        x1 = board.positions[(6,5)]
        x2 = board.positions[(7,5)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(0,4)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (0, 4)),
                         (p1 | p2 | x1 | board.positions[(0,4)], x2, 1, 2))

    def test_no_west_wrapped_capture(self):
        p1 = sum(board.positions[x] for x in [(4,4)])
        p2 = sum(board.positions[x] for x in [(4,5), (4,6)])

        x1 = board.positions[(3,1)]
        x2 = board.positions[(3,0)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(4,7)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (4, 7)),
                         (p1 | p2 | x1 | board.positions[(4,7)], x2, 1, 2))

        x1 = board.positions[(4,1)]
        x2 = board.positions[(4,0)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(4,7)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (4, 7)),
                         (p1 | p2 | x1 | board.positions[(4,7)], x2, 1, 2))

        x1 = board.positions[(5,1)]
        x2 = board.positions[(5,0)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(4,7)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (4, 7)),
                         (p1 | p2 | x1 | board.positions[(4,7)], x2, 1, 2))

    def test_no_south_wrapped_capture(self):
        p1 = sum(board.positions[x] for x in [(4,3)])
        p2 = sum(board.positions[x] for x in [(5,3), (6,3)])

        x1 = board.positions[(1,2)]
        x2 = board.positions[(0,2)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(7,3)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (7, 3)),
                         (p1 | p2 | x1 | board.positions[(7,3)], x2, 1, 2))

        x1 = board.positions[(1,3)]
        x2 = board.positions[(0,3)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(7,3)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (7, 3)),
                         (p1 | p2 | x1 | board.positions[(7,3)], x2, 1, 2))

        x1 = board.positions[(1,4)]
        x2 = board.positions[(0,4)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(7,3)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (7, 3)),
                         (p1 | p2 | x1 | board.positions[(7,3)], x2, 1, 2))

    def test_no_east_wrapped_capture(self):
        p1 = sum(board.positions[x] for x in [(3,3)])
        p2 = sum(board.positions[x] for x in [(3,1), (3,2)])

        x1 = board.positions[(2,6)]
        x2 = board.positions[(2,7)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(3,0)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (3, 0)),
                         (p1 | p2 | x1 | board.positions[(3,0)], x2, 1, 2))

        x1 = board.positions[(3,6)]
        x2 = board.positions[(3,7)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(3,0)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (3, 0)),
                         (p1 | p2 | x1 | board.positions[(3,0)], x2, 1, 2))

        x1 = board.positions[(4,6)]
        x2 = board.positions[(4,7)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(3,0)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (3, 0)),
                         (p1 | p2 | x1 | board.positions[(3,0)], x2, 1, 2))

    def test_no_northeast_wrapped_capture(self):
        p1 = sum(board.positions[x] for x in [(3,6)])
        p2 = sum(board.positions[x] for x in [(1,4), (2,5)])

        x1 = board.positions[(6,0)]
        x2 = board.positions[(7,1)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(0,3)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (0, 3)),
                         (p1 | p2 | x1 | board.positions[(0,3)], x2, 1, 1))

        x1 = board.positions[(6,1)]
        x2 = board.positions[(7,2)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(0,3)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (0, 3)),
                         (p1 | p2 | x1 | board.positions[(0,3)], x2, 1, 2))

        x1 = board.positions[(6,2)]
        x2 = board.positions[(7,3)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(0,3)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (0, 3)),
                         (p1 | p2 | x1 | board.positions[(0,3)], x2, 1, 2))

    def test_no_northwest_wrapped_capture(self):
        p1 = sum(board.positions[x] for x in [(3,1)])
        p2 = sum(board.positions[x] for x in [(1,3), (2,2)])

        x1 = board.positions[(6,5)]
        x2 = board.positions[(7,4)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(0,4)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (0, 4)),
                         (p1 | p2 | x1 | board.positions[(0,4)], x2, 1, 2))

        x1 = board.positions[(6,6)]
        x2 = board.positions[(7,5)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(0,4)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (0, 4)),
                         (p1 | p2 | x1 | board.positions[(0,4)], x2, 1, 2))

        x1 = board.positions[(6,7)]
        x2 = board.positions[(7,6)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(0,4)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (0, 4)),
                         (p1 | p2 | x1 | board.positions[(0,4)], x2, 1, 1))

    def test_no_southwest_wrapped_capture(self):
        p1 = sum(board.positions[x] for x in [(4,1)])
        p2 = sum(board.positions[x] for x in [(5,2), (6,3)])

        x1 = board.positions[(1,5)]
        x2 = board.positions[(0,4)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(7,4)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (7, 4)),
                         (p1 | p2 | x1 | board.positions[(7,4)], x2, 1, 2))

        x1 = board.positions[(1,6)]
        x2 = board.positions[(0,5)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(7,4)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (7, 4)),
                         (p1 | p2 | x1 | board.positions[(7,4)], x2, 1, 2))

        x1 = board.positions[(1,7)]
        x2 = board.positions[(0,6)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(7,4)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (7, 4)),
                         (p1 | p2 | x1 | board.positions[(7,4)], x2, 1, 1))

    def test_no_southeast_wrapped_capture(self):
        p1 = sum(board.positions[x] for x in [(4,6)])
        p2 = sum(board.positions[x] for x in [(5,5), (6,4)])

        x1 = board.positions[(1,0)]
        x2 = board.positions[(0,1)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(7,3)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (7, 3)),
                         (p1 | p2 | x1 | board.positions[(7,3)], x2, 1, 1))

        x1 = board.positions[(1,1)]
        x2 = board.positions[(0,2)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(7,3)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (7, 3)),
                         (p1 | p2 | x1 | board.positions[(7,3)], x2, 1, 2))

        x1 = board.positions[(1,2)]
        x2 = board.positions[(0,3)]
        self.assertEqual(board.legal_actions((p1 | x1, p2 | x2, 2, 1)), [(7,3)])
        self.assertEqual(board.next_state([(p1 | x1, p2 | x2, 2, 1)], (7, 3)),
                         (p1 | p2 | x1 | board.positions[(7,3)], x2, 1, 2))


if __name__ == '__main__':
    unittest.main()

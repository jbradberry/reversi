import re
import string


class Board(object):
    num_players = 2
    rows = cols = 8

    positions = {}

    str_pieces = {0: "   ", 1: " x ", 2: " o "}
    unicode_pieces = {0: "   ", 1: u" \u25cf ", 2: u" \u25cb "}

    moveRE = re.compile(r'([a-h])([1-8])')

    def __init__(self, *args, **kwargs):
        if not self.positions:
            self.initialize()

    @classmethod
    def initialize(cls):
        cls.positions.update(((r, c), 1 << (cls.cols * r + c))
                             for r in xrange(cls.rows)
                             for c in xrange(cls.cols))

    def start(self):
        # p1 placed, p2 placed, player to move
        return (self.positions[(3,4)] + self.positions[(4,3)],
                self.positions[(3,3)] + self.positions[(4,4)], 1)

    def display(self, state, play, _unicode=True):
        pieces = self.unicode_pieces if _unicode else self.str_pieces

        p1_placed, p2_placed, player = state

        row_sep = "  |" + "-"*(4*self.cols - 1) + "|\n"
        header = " "*4 + "   ".join(string.lowercase[:self.cols]) + "\n"
        msg = "Played: {0}\nPlayer {1} to move.    ({2}-{3})".format(
            self.pack(play), player,
            bin(p1_placed).count('1'), bin(p2_placed).count('1'))

        P = [[0 for c in xrange(self.cols)] for r in xrange(self.rows)]
        for (r, c), v in self.positions.iteritems():
            if v & p1_placed:
                P[r][c] = 1
            elif v & p2_placed:
                P[r][c] = 2

        board = row_sep.join("%d |"%(i+1) + "|".join(pieces[x] for x in row) +
                             "|\n" for i, row in enumerate(P))
        board = ''.join((header, row_sep, board, row_sep, header, msg))
        return board

    def is_legal(self, state, play):
        plays = set(self.legal_plays(state))
        return play in plays

    def next_player(self, state):
        return state[-1]

    def legal_plays(self, state):
        ## Kogge-Stone algorithm
        p1_placed, p2_placed, player = state
        occupied = p1_placed | p2_placed
        empty = 0xffffffffffffffff ^ occupied

        mask_a = 0xfefefefefefefefe
        mask_h = 0x7f7f7f7f7f7f7f7f

        mine = p1_placed if player == 1 else p2_placed
        opp = p2_placed if player == 1 else p1_placed
        legal = 0

        # N
        g, p = mine, opp
        g |= p & (g >> 8)
        p &= (p >> 8)
        g |= p & (g >> 16)
        p &= (p >> 16)
        g |= p & (g >> 32)
        legal |= ((g & ~mine) >> 8) & empty

        # S
        g, p = mine, opp
        g |= p & (g << 8)
        p &= (p << 8)
        g |= p & (g << 16)
        p &= (p << 16)
        g |= p & (g << 32)
        legal |= ((g & ~mine) << 8) & empty

        # E
        g, p = mine, opp & mask_a
        g |= p & (g << 1)
        p &= (p << 1)
        g |= p & (g << 2)
        p &= (p << 2)
        g |= p & (g << 4)
        legal |= ((g & ~mine & mask_h) << 1) & empty

        # W
        g, p = mine, opp & mask_h
        g |= p & (g >> 1)
        p &= (p >> 1)
        g |= p & (g >> 2)
        p &= (p >> 2)
        g |= p & (g >> 4)
        legal |= ((g & ~mine & mask_a) >> 1) & empty

        # NE
        g, p = mine, opp & mask_a
        g |= p & (g >> 7)
        p &= (p >> 7)
        g |= p & (g >> 14)
        p &= (p >> 14)
        g |= p & (g >> 28)
        legal |= ((g & ~mine & mask_h) >> 7) & empty

        # NW
        g, p = mine, opp & mask_h
        g |= p & (g >> 9)
        p &= (p >> 9)
        g |= p & (g >> 18)
        p &= (p >> 18)
        g |= p & (g >> 36)
        legal |= ((g & ~mine & mask_a) >> 9) & empty

        # SE
        g, p = mine, opp & mask_a
        g |= p & (g << 9)
        p &= (p << 9)
        g |= p & (g << 18)
        p &= (p << 18)
        g |= p & (g << 36)
        legal |= ((g & ~mine & mask_h) << 9) & empty

        # SW
        g, p = mine, opp & mask_h
        g |= p & (g << 7)
        p &= (p << 7)
        g |= p & (g << 14)
        p &= (p << 14)
        g |= p & (g << 28)
        legal |= ((g & ~mine & mask_a) << 7) & empty

        return [(r, c) for (r, c), v in self.positions.iteritems()
                if v & legal]

    def winner(self, state_lst):
        state = state_lst[-1]
        p1_placed, p2_placed, player = state

        if p2_placed == 0:
            return 1
        if p1_placed == 0:
            return 2

        occupied = p1_placed | p2_placed
        if (occupied == (1 << (self.rows * self.cols)) - 1 or
            not self.legal_plays(state)):
            p1_score = bin(p1_placed).count('1')
            p2_score = bin(p2_placed).count('1')
            if p1_score > p2_score:
                return 1
            if p2_score > p1_score:
                return 2
            if p1_score == p2_score:
                return 3
        return 0

    def winner_message(self, winner):
        if winner == 3:
            return "Stalemate."
        return "Winner: Player {0}.".format(winner)

    def parse(self, play):
        result = self.moveRE.match(play)
        if not result:
            return
        c, r = result.groups()
        return int(r) - 1, 'abcdefgh'.index(c)

    def pack(self, play):
        if play is None:
            return ''
        r, c = play
        return 'abcdefgh'[c] + str(r+1)

    def play(self, state, play):
        P = self.positions[play]
        p1_placed, p2_placed, player = state

        occupied = p1_placed | p2_placed
        empty = 0xffffffffffffffff ^ occupied

        mask_a = 0xfefefefefefefefe
        mask_h = 0x7f7f7f7f7f7f7f7f

        mine = p1_placed if player == 1 else p2_placed
        opp = p2_placed if player == 1 else p1_placed
        flips = 0

        # N
        g, p = P, opp
        g |= p & (g >> 8)
        p &= (p >> 8)
        g |= p & (g >> 16)
        p &= (p >> 16)
        g |= p & (g >> 32)
        if (g >> 8) & mine:
            flips |= g

        # S
        g, p = P, opp
        g |= p & (g << 8)
        p &= (p << 8)
        g |= p & (g << 16)
        p &= (p << 16)
        g |= p & (g << 32)
        if (g << 8) & mine:
            flips |= g

        # E
        g, p = P, opp & mask_a
        g |= p & (g << 1)
        p &= (p << 1)
        g |= p & (g << 2)
        p &= (p << 2)
        g |= p & (g << 4)
        if (g << 1) & mask_a & mine:
            flips |= g

        # W
        g, p = P, opp & mask_h
        g |= p & (g >> 1)
        p &= (p >> 1)
        g |= p & (g >> 2)
        p &= (p >> 2)
        g |= p & (g >> 4)
        if (g >> 1) & mask_h & mine:
            flips |= g

        # NE
        g, p = P, opp & mask_a
        g |= p & (g >> 7)
        p &= (p >> 7)
        g |= p & (g >> 14)
        p &= (p >> 14)
        g |= p & (g >> 28)
        if (g >> 7) & mask_a & mine:
            flips |= g

        # NW
        g, p = P, opp & mask_h
        g |= p & (g >> 9)
        p &= (p >> 9)
        g |= p & (g >> 18)
        p &= (p >> 18)
        g |= p & (g >> 36)
        if (g >> 9) & mask_h & mine:
            flips |= g

        # SE
        g, p = P, opp & mask_a
        g |= p & (g << 9)
        p &= (p << 9)
        g |= p & (g << 18)
        p &= (p << 18)
        g |= p & (g << 36)
        if (g << 9) & mask_a & mine:
            flips |= g

        # SW
        g, p = P, opp & mask_h
        g |= p & (g << 7)
        p &= (p << 7)
        g |= p & (g << 14)
        p &= (p << 14)
        g |= p & (g << 28)
        if (g << 7) & mask_h & mine:
            flips |= g

        mine |= flips
        opp &= ~flips
        p1_placed = mine if player == 1 else opp
        p2_placed = opp if player == 1 else mine

        if self.legal_plays((p1_placed, p2_placed, 3-player)):
            return (p1_placed, p2_placed, 3-player)
        return (p1_placed, p2_placed, player)

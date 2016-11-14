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

    def starting_state(self):
        # p1 placed, p2 placed, previous player, player to move
        return (self.positions[(3,4)] + self.positions[(4,3)],
                self.positions[(3,3)] + self.positions[(4,4)], 2, 1)

    def display(self, state, action, _unicode=True):
        pieces = self.unicode_pieces if _unicode else self.str_pieces

        p1_placed, p2_placed, previous, player = state

        # FIXME: new line above the board printout
        row_sep = "  |" + "-"*(4*self.cols - 1) + "|\n"
        header = " "*4 + "   ".join(string.lowercase[:self.cols]) + "\n"
        msg = "Played: {0}\nPlayer {1} to move.    ({2}-{3})".format(
            self.unpack_action(action), player,
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

    def is_legal(self, history, action):
        actions = set(self.legal_actions(history))
        return action in actions

    def legal_actions(self, history):
        ## Kogge-Stone algorithm
        p1_placed, p2_placed, previous, player = history[-1]
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

    def previous_player(self, state):
        return state[-2]

    def current_player(self, state):
        return state[-1]

    def is_ended(self, history):
        state = history[-1]
        p1_placed, p2_placed, previous, player = state

        if p2_placed == 0:
            return True
        if p1_placed == 0:
            return True

        occupied = p1_placed | p2_placed
        return (occupied == (1 << (self.rows * self.cols)) - 1 or
                not self.legal_actions([state]))

    def win_values(self, history):
        if not self.is_ended(history):
            return

        state = history[-1]
        p1_placed, p2_placed, previous, player = state

        p1_score = bin(p1_placed).count('1')
        p2_score = bin(p2_placed).count('1')

        if p1_score > p2_score:
            return {1: 1, 2: 0}
        if p2_score > p1_score:
            return {1: 0, 2: 1}
        if p1_score == p2_score:
            return {1: 0.5, 2: 0.5}

    def points_values(self, history):
        if not self.is_ended(history):
            return

        state = history[-1]
        p1_placed, p2_placed, previous, player = state

        p1_score = bin(p1_placed).count('1')
        p2_score = bin(p2_placed).count('1')

        return {1: p1_score, 2: p2_score}

    def winner_message(self, winners):
        winners = sorted((v, k) for k, v in winners.iteritems())
        value, winner = winners[-1]
        if value == 0.5:
            return "Tie."
        return "Winner: Player {0}.".format(winner)

    def pack_state(self, data):
        player = data['player']
        previous = data['previous_player']
        state = {1: 0, 2: 0}
        for item in data['pieces']:
            index = 1 << (self.cols * item['row'] + item['column'])
            state[item['player']] += index

        return (state[1], state[2], previous, player)

    def unpack_state(self, state):
        p1_placed, p2_placed, previous, player = state

        pieces = []
        for r in xrange(self.rows):
            for c in xrange(self.cols):
                index = 1 << (self.cols * r + c)
                if index & p1_placed:
                    pieces.append({'type': 'disc', 'player': 1, 'row': r, 'column': c})
                if index & p2_placed:
                    pieces.append({'type': 'disc', 'player': 2, 'row': r, 'column': c})

        return {
            'pieces': pieces,
            'player': player,
            'previous_player': previous,
        }

    def pack_action(self, notation):
        result = self.moveRE.match(notation)
        if not result:
            return
        c, r = result.groups()
        return int(r) - 1, 'abcdefgh'.index(c)

    def unpack_action(self, action):
        if action is None:
            return ''
        r, c = action
        return 'abcdefgh'[c] + str(r+1)

    def next_state(self, state, action):
        P = self.positions[action]
        p1_placed, p2_placed, previous, player = state

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

        # If there are legal actions with the next player, they are
        # next.  Otherwise, this player gets to go again.
        if self.legal_actions([(p1_placed, p2_placed, player, 3-player)]):
            return (p1_placed, p2_placed, player, 3-player)
        return (p1_placed, p2_placed, player, player)

class bishop:
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.side = side
        self.disabled = False
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'B'
        else:
            self.icon = 'b'

    def find_legal_moves(self, last_move):
        if(self.disabled == True):
            return set()
        
        legal_moves = set()

        i = self.row + 1
        k = self.col + 1
        while (i <= 7 and k <= 7 and self.board.board[i][k] == '.'):
            legal_moves.add((i, k))
            i += 1
            k += 1

        if (i <= 7 and k <= 7 and self.board.board[i][k] != '.' and self.board.check_ally(i, k, self.side) == False):
            legal_moves.add((i, k))

        i = self.row - 1
        k = self.col - 1
        while (i >= 0 and k >= 0 and self.board.board[i][k] == '.'):
            legal_moves.add((i, k))
            i -= 1
            k -= 1

        if (i >= 0 and k >= 0 and self.board.board[i][k] != '.' and self.board.check_ally(i, k, self.side) == False):
            legal_moves.add((i, k))

        i = self.row + 1
        k = self.col - 1
        while (i <= 7 and k >= 0 and self.board.board[i][k] == '.'):
            legal_moves.add((i, k))
            i += 1
            k -= 1

        if (i <= 7 and k >= 0 and self.board.board[i][k] != '.' and self.board.check_ally(i, k, self.side) == False):
            legal_moves.add((i, k))

        i = self.row - 1
        k = self.col + 1
        while (i >= 0 and k <= 7 and self.board.board[i][k] == '.'):
            legal_moves.add((i, k))
            i -= 1
            k += 1

        if (i >= 0 and k <= 7 and self.board.board[i][k] != '.' and self.board.check_ally(i, k, self.side) == False):
            legal_moves.add((i, k))

        return legal_moves
        
    def set_piece(self):
        self.board.set_piece((self.row, self.col), self)

    def move_piece(self, row, col, last_move):
        self.board.remove_piece((self.row, self.col))
        self.board.set_piece((row, col), self)
        self.board.increment_num_moves()
        self.board.save_board_states()
        last_move['icon'] = self.icon
        
        last_move['distance'] = 1
        
        last_move['row'] = row
        last_move['col'] = col

        self.row = row
        self.col = col

    def return_coord(self):
        return (self.row, self.col)

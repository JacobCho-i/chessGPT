class knight:
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.side = side
        self.disabled = False
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'N'
        else:
            self.icon = 'n'
    
    def find_legal_moves(self, last_move):
        if(self.disabled == True):
            return set()
        
        legal_moves = set()

        if (self.row >= 1):
            if (self.col >= 2 and self.board.check_ally(self.row-1, self.col-2, self.side) == False):
                legal_moves.add((self.row - 1, self.col - 2))
            if (self.col <= 5 and self.board.check_ally(self.row-1, self.col+2, self.side) == False):
                legal_moves.add((self.row - 1, self.col + 2))

        if (self.row <= 6):
            if (self.col >= 2 and self.board.check_ally(self.row+1, self.col-2, self.side) == False):
                legal_moves.add((self.row + 1, self.col - 2))
            if (self.col <= 5 and self.board.check_ally(self.row+1, self.col+2, self.side) == False):
                legal_moves.add((self.row + 1, self.col + 2))

        if (self.col >= 1):
            if (self.row >= 2 and self.board.check_ally(self.row-2, self.col-1, self.side) == False):
                legal_moves.add((self.row - 2, self.col - 1))
            if (self.row <= 5 and self.board.check_ally(self.row+2, self.col-1, self.side) == False):
                legal_moves.add((self.row + 2, self.col - 1))

        if (self.col <= 6):
            if (self.row >= 2 and self.board.check_ally(self.row-2, self.col+1, self.side) == False):
                legal_moves.add((self.row - 2, self.col + 1))
            if (self.row <= 5 and self.board.check_ally(self.row+2, self.col+1, self.side) == False):
                legal_moves.add((self.row + 2, self.col + 1))

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
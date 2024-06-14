import queen

class pawn:
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.side = side
        self.disabled = False
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'P'
        else:
            self.icon = 'p'

    def find_legal_moves(self, last_move):
        if self.disabled == True:
            return set()
        
        legal_moves = set()

        if (self.side == 'W' and self.board.board[self.row+1][self.col] == '.'):
            if (self.row == 1 and self.board.board[self.row+2][self.col] == '.'):
                legal_moves.add((self.row + 2, self.col))

        if (self.side == 'B' and self.board.board[self.row-1][self.col] == '.'):
            if (self.row == 6 and self.board.board[self.row-2][self.col] == '.'):
                legal_moves.add((self.row - 2, self.col)) 

        if self.side == 'W' and self.board.board[self.row+1][self.col] == '.' and (self.board.check_ally(self.row+1, self.col, self.side) == False):
            legal_moves.add((self.row+1, self.col))
        elif self.side == 'B' and self.board.board[self.row-1][self.col] == '.' and (self.board.check_ally(self.row-1, self.col, self.side) == False):
            legal_moves.add((self.row-1, self.col))

        if (self.col >= 1):
            if self.side == 'W' and (self.board.check_ally(self.row+1, self.col-1, self.side) == False) and self.board.board[self.row+1][self.col - 1] != '.':
                legal_moves.add((self.row+1, self.col-1))
            elif self.side == 'B' and (self.board.check_ally(self.row-1, self.col-1, self.side) == False) and self.board.board[self.row-1][self.col - 1] != '.':
                legal_moves.add((self.row-1, self.col-1))

        if (self.col < 7):
            if self.side == 'W' and (self.board.check_ally(self.row+1, self.col+1, self.side) == False) and self.board.board[self.row+1][self.col + 1] != '.':
                legal_moves.add((self.row+1, self.col+1))
            elif self.side == 'B' and (self.board.check_ally(self.row-1, self.col+1, self.side) == False) and self.board.board[self.row-1][self.col + 1] != '.':
                legal_moves.add((self.row-1, self.col+1))

        if ((last_move['icon'] == 'p' or last_move['icon'] == 'P') and (last_move['distance'] == 2) and (last_move['row'] == self.row and last_move['col'] + 1 == self.col)):
            if self.side == 'W' and (self.board.check_ally(self.row+1, self.col-1, self.side) == False) and (self.board.check_ally(self.row+1, self.col-1, self.side) == False):
                legal_moves.add((self.row+1, self.col-1))
            elif self.side == 'B' and (self.board.check_ally(self.row-1, self.col-1, self.side) == False) and (self.board.check_ally(self.row-1, self.col-1, self.side) == False):
                legal_moves.add((self.row-1, self.col-1))

        if ((last_move['icon'] == 'p' or last_move['icon'] == 'P') and (last_move['distance'] == 2) and (last_move['row'] == self.row and last_move['col'] - 1 == self.col)):
            if self.side == 'W' and (self.board.check_ally(self.row+1, self.col+1, self.side) == False):
                legal_moves.add((self.row+1, self.col+1))
            elif self.side == 'B' and (self.board.check_ally(self.row-1, self.col+1, self.side) == False):
                legal_moves.add((self.row-1, self.col+1))

        return legal_moves
    

    def set_piece(self):
        self.board.set_piece((self.row, self.col), self)

    def move_piece(self, row, col, last_move):
        self.board.remove_piece((self.row, self.col))
        self.board.set_piece((row, col), self)
        self.board.increment_num_moves()
        self.board.save_board_states()
        last_move['icon'] = self.icon
        
        if (self.col == col):
            last_move['distance'] = abs(self.row - row)
        else:
            last_move['distance'] = 1
        
        last_move['row'] = row
        last_move['col'] = col

        if((self.side == 'W' or self.side == 'w') and row == 7):
            self.disabled = True
            new_queen = queen(self.board, row, col, 'W')
            self.board.pieces['white_pieces'].append(new_queen)
            self.board.set_piece((row, col), new_queen)
        elif((self.side == 'B' or self.side == 'b') and row == 0):
            self.disabled = True
            new_queen = queen(self.board, row, col, 'B')
            self.board.pieces['black_pieces'].append(new_queen)
            self.board.set_piece((row, col), new_queen)

        self.row = row
        self.col = col

    def return_coord(self):
        return (self.row, self.col)
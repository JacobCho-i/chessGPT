class king:
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.side = side
        self.disabled = False
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'K'
        else:
            self.icon = 'k'
    
    def find_legal_moves(self, last_move):
        if self.disabled == True:
            return set()
        
        legal_moves = set()
        
        if (self.col >= 1 and self.board.check_ally(self.row, self.col-1, self.side) == False): 
            legal_moves.add((self.row, self.col - 1))

        if (self.col <= 6 and self.board.check_ally(self.row, self.col+1, self.side) == False): 
            legal_moves.add((self.row, self.col + 1))

        if (self.row >= 1 and self.board.check_ally(self.row-1, self.col, self.side) == False): 
            legal_moves.add((self.row - 1, self.col))

        if (self.row <= 6 and self.board.check_ally(self.row+1, self.col, self.side) == False): 
            legal_moves.add((self.row + 1, self.col))

        if (self.row >= 1 and self.col >= 1 and self.board.check_ally(self.row-1, self.col-1, self.side) == False): 
            legal_moves.add((self.row - 1, self.col - 1))

        if (self.row <= 6 and self.col <= 6 and self.board.check_ally(self.row+1, self.col+1, self.side) == False): 
            legal_moves.add((self.row + 1, self.col + 1))

        if (self.row <= 6 and self.col >= 1 and self.board.check_ally(self.row+1, self.col-1, self.side) == False): 
            legal_moves.add((self.row + 1, self.col - 1))
            
        if (self.row >= 1 and self.col <= 6 and self.board.check_ally(self.row-1, self.col+1, self.side) == False): 
            legal_moves.add((self.row - 1, self.col + 1))
        
        if(self.side == 'W' or self.side == 'w'):
            if(self.board.white_left_castle == True):
                legal_moves.add((self.row, self.col - 2))
            if(self.board.white_right_castle == True):
                legal_moves.add((self.row, self.col + 2))
        else:
            if(self.board.black_left_castle == True):
                legal_moves.add((self.row, self.col - 2))
            if(self.board.black_right_castle == True):
                legal_moves.add((self.row, self.col + 2))
        
        return legal_moves
    
    def set_piece(self):
        self.board.set_piece((self.row, self.col), self)

    def move_piece(self, row, col, last_move):
        self.board.remove_piece((self.row, self.col))
        self.board.set_piece((row, col), self)

        if(self.row == 0 and self.col == 4):
            if(row == 0 and col == 2):
                rook = self.board.board[0][0]
                self.board.remove_piece((0, 0))
                rook.move_piece(0, 3, last_move)
            elif(row == 0 and col == 6):
                rook = self.board.board[0][7]
                self.board.remove_piece((0, 7))
                rook.move_piece(0, 5, last_move)
            
        elif(self.row == 7 and self.col == 4):
            if(row == 0 and col == 2):
                rook = self.board.board[7][0]
                self.board.remove_piece((7, 0))
                rook.move_piece(7, 3, last_move)
            elif(row == 0 and col == 6):
                rook = self.board.board[7][7]
                self.board.remove_piece((7, 7))
                rook.move_piece(7, 5, last_move)
            
        if ((self.row == 0 and self.col == 4) or (self.row == 7 and self.col == 4)):
            self.board.disable_castle(self.row, self.col)

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
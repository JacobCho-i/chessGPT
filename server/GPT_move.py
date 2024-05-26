import os
import time
import chess
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

#AI prompt: make a move as white based on this chess position, give the move notation in the format of (original square, new square) without additional text

#TODO: Check, legal moves, rules (low prio) 

def ask_gpt(client, move_list, board, error_str = "", side = "black"):
    try:
        move_str = ' '.join(move_list)
        completion = client.chat.completions.create(
            model = "gpt-4",
            messages = [
                {"role": "system", "content": "You are a chess master that will make good chess moves"},
                {"role": "user", "content":  error_str + move_str + " based on the game moves given, make one chess move on " + side + " side, only return the chess notation without any additional words"}
            ]
        )
        
        reply = completion.choices[0].message.content

        response = reply

        if ('.' in reply):
            temp = reply.split('.')
            response = temp[-1]
        
        if (' ' in reply):
            temp = reply.split(' ')
            response = temp[-1]

        if (len(response) > 7 or response == None or ' ' in response or ('-' in response and 'O' not in response)):
            print(len(response))
            ask_gpt(client, move_list, board, side = side)

        else:
            try:
                board.parse_san(response)
                print(response)
                move_list.append(response)
                return response
            
            except:
                print(response)
                print(move_list)
                print("ChatGPT made an illegal move")
                error_str = response + " was an illegal move! "
                ask_gpt(client, move_list, board, error_str, side)
        
    except:
        print("Waiting for ChatGPT...")
        time.sleep(10)
        ask_gpt(client, move_list, board, side = side)



def get_web_notation(str, board): #input e4, returns e2:e4
    move_object = board.parse_san(str)
    uci_notation = board.uci(move_object)
    temp1 = uci_notation[:2]
    temp2 = uci_notation[2:]
    move_notation = temp1 + ":" + temp2
    return move_notation


def get_gpt_notation(str, board): #input e2:e4, returns e4
    temp = str.split(':')
    temp = ''.join(temp)
    algebraic_notation = board.parse_uci(temp)
    standard_notation = board.san(algebraic_notation)
    return standard_notation


def move(str, client, board, move_list):
    player_move = get_gpt_notation(str, board)
    m.append(player_move)
    board.push_san(player_move)
    print(board)
    print("---------------")
    gpt_move = ask_gpt(client, m, board, side = "black")
    gpt_move_moded_notation = get_web_notation(gpt_move, board)
    board.push_san(gpt_move)
    print(board)
    return gpt_move_moded_notation

####################################################################################
class board:

    def create_empty_board(self):
        board = []
        for i in range(0, 8):
            row = []
            for j in range(0, 8):
                row.append('.')
            board.append(row)
        return board

    def __init__(self):
        self.visual_board = self.create_empty_board()
        
        self.board = self.create_empty_board()
        
        self.board_states = []
        self.num_moves = 0

        self.black_left_castle = True
        self.black_right_castle = True
        self.white_left_castle = True
        self.white_right_castle = True

    
    def disable_castle(self, row, col):

        if (row == 0 and col == 4):
            self.white_left_castle = False
            self.white_right_castle = False

        elif (row == 7 and col == 4):
            self.black_left_castle = False
            self.black_right_castle = False

        elif (row == 0 and col == 0):
            self.white_left_castle = False

        elif (row == 0 and col == 7):
            self.white_right_castle = False

        elif (row == 7 and col == 0):
            self.black_left_castle = False

        elif (row == 7 and col == 7):
            self.black_right_castle = False

    def return_castle_states(self):
        states = {'black_left':self.black_left_castle, 'black_right':self.black_right_castle, 'white_left':self.white_left_caslte, 'white_right':self.white_right_castle}
        return states
        

    def check_ally(self, row, col, side):
        if self.board[row][col] == '.':
            return False
        
        elif self.board[row][col].side != side:
            return False
        else:
            return True
        
    def check_enemy_king(self, row, col):
        count = 0
        #if(self.visual_board[row][col] == 'K' or self.visual_board[row][col] == 'k'):
           # count += 1

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 1 and j == 1):
                    continue

                if (self.visual_board[row + i][col + j].lower() == 'k'):
                    count += 1

        if (count == 1):
            return False

        return True
    
    def set_piece(self, coord, piece):
        self.visual_board[coord[0]][coord[1]] = piece.icon
        self.board[coord[0]][coord[1]] = piece

    def increment_num_moves(self):
        self.num_moves += 1

    def return_num_moves(self):
        return self.num_moves

    def remove_piece(self, coord):
        self.board[coord[0]][coord[1]] = "."
        self.visual_board[coord[0]][coord[1]] = "."
    
    def return_board(self):
        return self.board
    
    def return_visual_board(self):
        visual = ''
        i = len(self.visual_board) - 1
        while i > 0:
            temp = ' '.join(self.visual_board[i])
            visual += temp
            visual += '\n'
            i -= 1
        visual += ' '.join(self.visual_board[0])
        return visual
    
    def save_board_states(self):
        self.board_states.append(self.return_visual_board())

    def return_board_states(self):
        return self.board_states
    
    def print_board_states(self):
        print('_______________')
        for i in range(self.num_moves):
            print(i)
            print(self.board_states[i])
            print('_______________')
    
    def print_board(self):
        print('    _______________')
        i = len(self.visual_board) - 1
        while i >= 0:
            temp = ' '.join(self.visual_board[i])
            print(str(i) + ' | ' + temp)
            i -= 1
        print('  | _______________')
        print('    0 1 2 3 4 5 6 7')


class pawn:
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.legal_moves = set()
        self.side = side
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'P'
        else:
            self.icon = 'p'

    def find_legal_moves(self, last_move):
        temp = self.row

        if (self.side == 'W' and self.board.board[temp+1][self.col] == '.'):
            if (self.row == 1 and self.board.board[temp+2][self.col] == '.'):
                self.legal_moves.add((temp+2, self.col))

        if (self.side == 'B' and self.board.board[temp-1][self.col] == '.'):
            if (self.row == 6 and self.board.board[temp-2][self.col] == '.'):
                self.legal_moves.add((temp-2, self.col)) 

        if self.side == 'W' and self.board.board[temp+1][self.col] == '.' and (self.board.check_ally(temp+1, self.col, self.side) == False):
            self.legal_moves.add((temp+1, self.col))
        elif self.side == 'B' and self.board.board[temp-1][self.col] == '.' and (self.board.check_ally(temp-1, self.col, self.side) == False):
            self.legal_moves.add((temp-1, self.col))

        if (self.col >= 1):
            if self.side == 'W' and (self.board.check_ally(temp+1, self.col-1, self.side) == False) and self.board.board[temp+1][self.col - 1] != '.':
                self.legal_moves.add((temp+1, self.col-1))
            elif self.side == 'B' and (self.board.check_ally(temp-1, self.col-1, self.side) == False) and self.board.board[temp-1][self.col - 1] != '.':
                self.legal_moves.add((temp-1, self.col-1))

        if (self.col < 7):
            if self.side == 'W' and (self.board.check_ally(temp+1, self.col+1, self.side) == False) and self.board.board[temp+1][self.col + 1] != '.':
                self.legal_moves.add((temp+1, self.col+1))
            elif self.side == 'B' and (self.board.check_ally(temp-1, self.col+1, self.side) == False) and self.board.board[temp-1][self.col + 1] != '.':
                self.legal_moves.add((temp-1, self.col+1))

        if ((last_move['icon'] == 'p' or last_move['icon'] == 'P') and (last_move['distance'] == 2) and (last_move['row'] == self.row and last_move['col'] + 1 == self.col)):
            if self.side == 'W' and (self.board.check_ally(temp+1, self.col-1, self.side) == False) and (self.board.check_ally(temp+1, self.col-1, self.side) == False):
                self.legal_moves.add((temp+1, self.col-1))
            elif self.side == 'B' and (self.board.check_ally(temp-1, self.col-1, self.side) == False) and (self.board.check_ally(temp-1, self.col-1, self.side) == False):
                self.legal_moves.add((temp-1, self.col-1))

        if ((last_move['icon'] == 'p' or last_move['icon'] == 'P') and (last_move['distance'] == 2) and (last_move['row'] == self.row and last_move['col'] - 1 == self.col)):
            if self.side == 'W' and (self.board.check_ally(temp+1, self.col+1, self.side) == False):
                self.legal_moves.add((temp+1, self.col+1))
            elif self.side == 'B' and (self.board.check_ally(temp-1, self.col+1, self.side) == False):
                self.legal_moves.add((temp-1, self.col+1))

        return self.legal_moves
    

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

        self.row = row
        self.col = col

    def return_coord(self):
        return (self.row, self.col)


class king:
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.legal_moves = set()
        self.side = side
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'K'
        else:
            self.icon = 'k'
    
    def find_legal_moves(self, last_move):
        if (self.col >= 1 and self.board.check_ally(self.row, self.col-1, self.side) == False and self.board.check_enemy_king(self.row, self.col - 1) == False): 
            self.legal_moves.add((self.row, self.col - 1))

        if (self.col <= 6 and self.board.check_ally(self.row, self.col+1, self.side) == False and self.board.check_enemy_king(self.row, self.col + 1) == False): 
            self.legal_moves.add((self.row, self.col + 1))

        if (self.row >= 1 and self.board.check_ally(self.row-1, self.col, self.side) == False and self.board.check_enemy_king(self.row - 1, self.col) == False): 
            self.legal_moves.add((self.row - 1, self.col))

        if (self.row <= 6 and self.board.check_ally(self.row+1, self.col, self.side) == False and self.board.check_enemy_king(self.row + 1, self.col) == False): 
            self.legal_moves.add((self.row + 1, self.col))

        if (self.row >= 1 and self.col >= 1 and self.board.check_ally(self.row-1, self.col-1, self.side) == False and self.board.check_enemy_king(self.row - 1, self.col - 1) == False): 
            self.legal_moves.add((self.row - 1, self.col - 1))

        if (self.row <= 6 and self.col <= 6 and self.board.check_ally(self.row+1, self.col+1, self.side) == False and self.board.check_enemy_king(self.row + 1, self.col + 1) == False): 
            self.legal_moves.add((self.row + 1, self.col + 1))

        if (self.row <= 6 and self.col >= 1 and self.board.check_ally(self.row+1, self.col-1, self.side) == False and self.board.check_enemy_king(self.row + 1, self.col - 1) == False): 
            self.legal_moves.add((self.row + 1, self.col - 1))
            
        if (self.row >= 1 and self.col <= 6 and self.board.check_ally(self.row-1, self.col+1, self.side) == False and self.board.check_enemy_king(self.row - 1, self.col + 1) == False): 
            self.legal_moves.add((self.row - 1, self.col + 1))

        return self.legal_moves
    
    def set_piece(self):
        self.board.set_piece((self.row, self.col), self)

    def move_piece(self, row, col, last_move):
        self.board.remove_piece((self.row, self.col))
        self.board.set_piece((row, col), self.icon)
        self.board.increment_num_moves()
        self.board.save_board_states()
        if ((self.row == 0 and self.col == 4) or (self.row == 7 and self.col == 4)):
            self.board.disable_castle(self.row, self.col)

        last_move['icon'] = self.icon
        
        last_move['distance'] = 1
        
        last_move['row'] = row
        last_move['col'] = col

        self.row = row
        self.col = col

    def return_coord(self):
        return (self.row, self.col)
    

class rook:
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.legal_moves = set()
        self.side = side
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'R'
        else:
            self.icon = 'r'

    def find_legal_moves(self, last_move):
        i = self.row + 1
        while (i <= 7 and self.board.board[i][self.col] == '.'):
            self.legal_moves.add((i, self.col))
            i += 1

        if (i <= 7 and self.board.board[i][self.col] != '.' and self.board.check_ally(i, self.col, self.side) == False):
            self.legal_moves.add((i, self.col))

        i = self.row - 1
        while (i >= 0 and self.board.board[i][self.col] == '.'):
            self.legal_moves.add((i, self.col))
            i -= 1

        if (i >= 0 and self.board.board[i][self.col] != '.' and self.board.check_ally(i, self.col, self.side) == False):
            self.legal_moves.add((i, self.col))

        k = self.col + 1
        while (k <= 7 and self.board.board[self.row][k] == '.'):
            self.legal_moves.add((self.row, k))
            k += 1

        if (k <= 7 and self.board.board[self.row][k] != '.' and self.board.check_ally(self.row, k, self.side) == False):
            self.legal_moves.add((self.row, k))

        k = self.col - 1
        while (k >= 0 and self.board.board[self.row][k] == '.'):
            self.legal_moves.add((self.row, k))
            k -= 1

        if (k >= 0 and self.board.board[self.row][k] != '.' and self.board.check_ally(self.row, k, self.side) == False):
            self.legal_moves.add((self.row, k))

        return self.legal_moves
    
    def set_piece(self):
        self.board.set_piece((self.row, self.col), self)

    def move_piece(self, row, col, last_move):
        self.board.remove_piece((self.row, self.col))
        self.board.set_piece((row, col), self.icon)
        self.board.increment_num_moves()
        self.board.save_board_states()
        if ((self.row == 7 and self.col == 0) or (self.row == 7 and self.col == 7) or (self.row == 0 and self.col == 0) or (self.row == 0 and self.col == 7)):
            self.board.disable_castle(self.row, self.col)
            
        last_move['icon'] = self.icon
        
        last_move['distance'] = 1
        
        last_move['row'] = row
        last_move['col'] = col

        self.row = row
        self.col = col

    def return_coord(self):
        return (self.row, self.col)
    
class bishop:
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.legal_moves = set()
        self.side = side
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'B'
        else:
            self.icon = 'b'

    def find_legal_moves(self, last_move):
        i = self.row + 1
        k = self.col + 1
        while (i <= 7 and k <= 7 and self.board.board[i][k] == '.'):
            self.legal_moves.add((i, k))
            i += 1
            k += 1

        if (i <= 7 and k <= 7 and self.board.board[i][k] != '.' and self.board.check_ally(i, k, self.side) == False):
            self.legal_moves.add((i, k))

        i = self.row - 1
        k = self.col - 1
        while (i >= 0 and k >= 0 and self.board.board[i][k] == '.'):
            self.legal_moves.add((i, k))
            i -= 1
            k -= 1

        if (i >= 0 and k >= 0 and self.board.board[i][k] != '.' and self.board.check_ally(i, k, self.side) == False):
            self.legal_moves.add((i, k))

        i = self.row + 1
        k = self.col - 1
        while (i <= 7 and k >= 0 and self.board.board[i][k] == '.'):
            self.legal_moves.add((i, k))
            i += 1
            k -= 1

        if (i <= 7 and k >= 0 and self.board.board[i][k] != '.' and self.board.check_ally(i, k, self.side) == False):
            self.legal_moves.add((i, k))

        i = self.row - 1
        k = self.col + 1
        while (i >= 0 and k <= 7 and self.board.board[i][k] == '.'):
            self.legal_moves.add((i, k))
            i -= 1
            k += 1

        if (i >= 0 and k <= 7 and self.board.board[i][k] != '.' and self.board.check_ally(i, k, self.side) == False):
            self.legal_moves.add((i, k))

        return self.legal_moves
        
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


class knight:
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.legal_moves = set()
        self.side = side
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'N'
        else:
            self.icon = 'n'
    
    def find_legal_moves(self, last_move):
        if (self.row >= 1):
            if (self.col >= 2 and self.board.check_ally(self.row-1, self.col-2, self.side) == False):
                self.legal_moves.add((self.row - 1, self.col - 2))
            if (self.col <= 5 and self.board.check_ally(self.row-1, self.col+2, self.side) == False):
                self.legal_moves.add((self.row - 1, self.col + 2))

        if (self.row <= 6):
            if (self.col >= 2 and self.board.check_ally(self.row+1, self.col-2, self.side) == False):
                self.legal_moves.add((self.row + 1, self.col - 2))
            if (self.col <= 5 and self.board.check_ally(self.row+1, self.col+2, self.side) == False):
                self.legal_moves.add((self.row + 1, self.col + 2))

        if (self.col >= 1):
            if (self.row >= 2 and self.board.check_ally(self.row-2, self.col-1, self.side) == False):
                self.legal_moves.add((self.row - 2, self.col - 1))
            if (self.row <= 5 and self.board.check_ally(self.row+2, self.col-1, self.side) == False):
                self.legal_moves.add((self.row + 2, self.col - 1))

        if (self.col <= 6):
            if (self.row >= 2 and self.board.check_ally(self.row-2, self.col+1, self.side) == False):
                self.legal_moves.add((self.row - 2, self.col + 1))
            if (self.row <= 5 and self.board.check_ally(self.row+2, self.col+1, self.side) == False):
                self.legal_moves.add((self.row + 2, self.col + 1))

        return self.legal_moves
    
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


class queen:
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.legal_moves = set()
        self.side = side
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'Q'
        else:
            self.icon = 'q'

    def find_legal_moves(self, last_move):
        i = self.row + 1
        k = self.col + 1
        while (i <= 7 and k <= 7 and self.board.board[i][k] == '.'):
            self.legal_moves.add((i, k))
            i += 1
            k += 1

        if (i <= 7 and k <= 7 and self.board.board[i][k] != '.' and self.board.check_ally(i, k, self.side) == False):
            self.legal_moves.add((i, k))

        i = self.row - 1
        k = self.col - 1
        while (i >= 0 and k >= 0 and self.board.board[i][k] == '.'):
            self.legal_moves.add((i, k))
            i -= 1
            k -= 1

        if (i >= 0 and k >= 0 and self.board.board[i][k] != '.' and self.board.check_ally(i, k, self.side) == False):
            self.legal_moves.add((i, k))

        i = self.row + 1
        k = self.col - 1
        while (i <= 7 and k >= 0 and self.board.board[i][k] == '.'):
            self.legal_moves.add((i, k))
            i += 1
            k -= 1

        if (i <= 7 and k >= 0 and self.board.board[i][k] != '.' and self.board.check_ally(i, k, self.side) == False):
            self.legal_moves.add((i, k))

        i = self.row - 1
        k = self.col + 1
        while (i >= 0 and k <= 7 and self.board.board[i][k] == '.'):
            self.legal_moves.add((i, k))
            i -= 1
            k += 1

        if (i >= 0 and k <= 7 and self.board.board[i][k] != '.' and self.board.check_ally(i, k, self.side) == False):
            self.legal_moves.add((i, k))

        i = self.row + 1
        while (i <= 7 and self.board.board[i][self.col] == '.'):
            self.legal_moves.add((i, self.col))
            i += 1

        if (i <= 7 and self.board.board[i][self.col] != '.' and self.board.check_ally(i, self.col, self.side) == False):
            self.legal_moves.add((i, self.col))

        i = self.row - 1
        while (i >= 0 and self.board.board[i][self.col] == '.'):
            self.legal_moves.add((i, self.col))
            i -= 1

        if (i >= 0 and self.board.board[i][self.col] != '.' and self.board.check_ally(i, self.col, self.side) == False):
            self.legal_moves.add((i, self.col))

        k = self.col + 1
        while (k <= 7 and self.board.board[self.row][k] == '.'):
            self.legal_moves.add((self.row, k))
            k += 1

        if (k <= 7 and self.board.board[self.row][k] != '.' and self.board.check_ally(self.row, k, self.side) == False):
            self.legal_moves.add((self.row, k))

        k = self.col - 1
        while (k >= 0 and self.board.board[self.row][k] == '.'):
            self.legal_moves.add((self.row, k))
            k -= 1

        if (k >= 0 and self.board.board[self.row][k] != '.' and self.board.check_ally(self.row, k, self.side) == False):
            self.legal_moves.add((self.row, k))

        return self.legal_moves
    
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

####################################################################################
def set_board(board):
    pieces = {}

    #white pieces
    R1 = rook(board, 0, 0, 'W')
    R2 = rook(board, 0, 7, 'W')

    N1 = knight(board, 0, 1, 'W')
    N2 = knight(board, 0, 6, 'W')

    B1 = bishop(board, 0, 2, 'W')
    B2 = bishop(board, 0, 5, 'W')

    Q = queen(board, 0, 3, 'W')

    K = king(board, 0, 4, 'W')

    Plist = []
    for i in range(0, 8):
        Plist.append(pawn(board, 1, i, 'B'))

    #black pieces
    r1 = rook(board, 7, 0, 'B')
    r2 = rook(board, 7, 7, 'B')

    n1 = knight(board, 7, 1, 'B')
    n2 = knight(board, 7, 6, 'B')

    b1 = bishop(board, 7, 2, 'B')
    b2 = bishop(board, 7, 5, 'B')

    q = queen(board, 7, 3, 'B')

    k = king(board, 7, 4, 'B')

    plist = []
    for i in range(0, 8):
        plist.append(pawn(board, 6, i, 'B'))
    
    #piece dictionary
    wp = [R1, R2, N1, N2, B1, B2, Q, K]
    bp = [r1, r2, n1, n2, b1, b2, q, k]
    for i in range (0, 8):
        wp.append(Plist[i])
        bp.append(plist[i])

    pieces.update({'white_pieces' : wp})
    pieces.update({'black_pieces' : bp})

    #set_pieces

    for i in pieces['white_pieces']:
        i.set_piece()

    for k in pieces['black_pieces']:
        k.set_piece()

    return pieces

####################################################################################


if __name__ == '__main__':  
    client = OpenAI()

    m = []

    #board = chess.Board()

    i = 0

    #test1 = get_web_notation("Nc3")
    #test2 = get_gpt_notation(test1)
    #print(test1)
    #print(test2)

    #print(move("e2:e4", client, board, m))
    
    b = board()
    k = king(b, 4, 4, 'B')
    K = king(b, 5, 5, 'W')
    k.set_piece()
    K.set_piece()
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}
    for i in k.find_legal_moves(last_move):
        b.visual_board[i[0]][i[1]] = '?'
    b.print_board()


    '''
    chess_board = set_board(b)
    print(chess_board)
    b.print_board()
    print("--------------------------")
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}
    chess_board['white_pieces'][12].move_piece(3, 4, last_move)
    print(last_move)
    print("--------------------------")
    chess_board['black_pieces'][12].move_piece(4, 4, last_move)
    print(b.return_visual_board())
    print(b.return_num_moves())
    print(b.return_board_states())
    b.print_board_states()

    '''
    '''
    for i in chess_board['white_pieces']:
        print(i.icon)
        for i in i.find_legal_moves(last_move):
            b.visual_board[i[0]][i[1]] = '?'
        b.print_board()

    for i in chess_board['black_pieces']:
        print(i.icon)
        for i in i.find_legal_moves(last_move):
            b.visual_board[i[0]][i[1]] = '?'
        b.print_board()
    '''

    #print(P3.find_legal_moves(last_move))
    #print(P3.return_coord())
    #print("--------------------------")
    #b.print_board()



    

    '''
    while board.is_checkmate() == False and board.is_stalemate() == False and board.is_insufficient_material() == False and board.is_seventyfive_moves() == False and board.can_claim_draw() == False:
        #m.append(player_move[i])
        #board.push_san(player_move[i])
        if i % 2 == 0:
            ask_gpt(client, m, board, side = "white")
        else:
            ask_gpt(client, m, board, side = "black")
        print(i, m)
        print(board)
        i += 1
    '''

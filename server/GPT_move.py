#import os
import time
import copy
#import chess
from openai import OpenAI
#from dotenv import load_dotenv
#load_dotenv()

#AI prompt: make a move as white based on this chess position, give the move notation in the format of (original square, new square) without additional text

def ask_gpt(client, move_str, board, error_str = "", side = "black"):
    #try:
    completion = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {"role": "system", "content": "You are a chess master that will make good chess moves"},
            {"role": "user", "content":  error_str + "last move was " + move_str + ", based on the game moves given, make one chess move on " + side + " side, return the move in the format of tuple(starting coordinate, end coordinate) without additional texts"}
        ]
    )
    
    reply = completion.choices[0].message.content

    response = reply
    response = response.replace("(", "")
    response = response.replace(")", "")
    response = response.replace("'", "")
    response = response.replace("\"", "")
    '''
    if ('.' in reply):
        temp = reply.split('.')
        response = temp[-1]
    
    if (' ' in reply):
        temp = reply.split(' ')
        response = temp[-1]

    if (len(response) > 7 or response == None or ('-' in response and 'O' in response)):
        print(len(response))
        ask_gpt(client, move_list, board, side = side)
    '''
    if(len(response) > 10 or "," not in response):
        print(response)
        time.sleep(5)
        return ask_gpt(client, move_str, board, "only return the tuple(starting coordinate, end coordinate) ")
    else:
        try:
            #board.parse_san(response)
            #print(response)
            #move_list.append(response)
            #return response
            
            #move = response.replace("(", "")
            #move = move.replace(")", "")
            move = response.split(", ")
            start = move[0]
            print("start: ", start)
            end = move[1]
            print("end: ", end)
            return [start, end, get_coords(start), get_coords(end), reply]
            #start_coord = get_coords(start)
            #end_coord = get_coords(end)
            #print("return: ", start, end, start_coord, end_coord)
            
        
        except:
            print(response)
            time.sleep(5)
            return ask_gpt(client, move_str, board, "only return the tuple(starting coordinate, end coordinate) ")
            #print("ChatGPT made an illegal move")
            #error_str = response + " was an illegal move! "
            #ask_gpt(client, move_list, board, error_str, side)
    '''   
    except:
        print("Waiting for ChatGPT...")
        time.sleep(5)
        return ask_gpt(client, move_list, board, "only return the tuple(starting coordinate, end coordinate) ")
    '''

def get_coords(notation):
    print("get_coords: ", notation)
    match notation[0]:
        case 'a':
            col = 0
        case 'b':
            col = 1
        case 'c':
            col = 2
        case 'd':
            col = 3
        case 'e':
            col = 4
        case 'f':
            col = 5
        case 'g':
            col = 6
        case 'h':
            col = 7
    
    return (int(notation[1]) - 1, col)
    
'''
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
'''
####################################################################################
class board:
    def __init__(self):
        self.visual_board = [
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.']
                     ]
        
        self.board = [
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.']
                     ]
        
        self.board_states = []
        self.num_moves = 0

        self.pieces = set_board(self)

        self.black_left_castle = True
        self.black_right_castle = True
        self.white_left_castle = True
        self.white_right_castle = True


    def return_pieces(self):
        return self.pieces
    
    
    def check_mate(self, side, last_move):
        if(self.in_check(side, last_move) == False):
            return False
        else:
            if(side == 'W' or side == 'w'):
                for i in b.pieces['black_pieces']:
                    for j in i.find_legal_moves(last_move):
                        if(self.pre_check(side, i.row, i.col, j[0], j[1], last_move) == False):
                            return False
                return True
            elif(side == 'B' or side == 'b'):
                for i in b.pieces['white_pieces']:
                    for j in i.find_legal_moves(last_move):
                        if(self.pre_check(side, i.row, i.col, j[0], j[1], last_move) == False):
                            return False
                return True
    
    def in_check(self, side, last_move):
        if(side == 'W' or side == 'w'):
            king = self.pieces['white_pieces'][7]
            possible_moves = self.find_all_legal_moves('B', last_move)
            if((king.return_coord()) in possible_moves):
                print("In check: ", king.return_coord())
                return True
            else:
                return False

        else:
            king = self.pieces['black_pieces'][7]
            possible_moves = self.find_all_legal_moves('W', last_move)
            if((king.return_coord()) in possible_moves):
                return True
            else:
                return False
        
    def pre_check(self, side, curr_row, curr_col, row, col, last_move):        
        b = board()
        
        b.board = copy.deepcopy(self.board)
        b.visual_board = copy.deepcopy(self.visual_board)
        b.pieces = copy.deepcopy(self.pieces)

        for i in b.pieces['white_pieces']:
            i.board = b
        
        for i in b.pieces['black_pieces']:
            i.board = b

        for i in b.board:
            for j in i:
                if(j != '.'):
                    j.board = b
        

        piece1 = b.board[curr_row][curr_col]
        piece2 = b.board[row][col]

        b.remove_piece((curr_row, curr_col))
        if(piece1 != '.'):
            #b.set_piece((row, col), piece1)
            if(piece2 != '.'):
                b.remove_piece((row, col))
            piece1.move_piece(row, col, last_move)

        if(piece2 != '.'):
            piece2.disable = True

        '''
        if(side == 'W'):
            for i in b.pieces['white_pieces']:
                if i.row == curr_row and i.col == curr_col:
                    i.row = row
                    i.col = col
        else:
            for i in b.pieces['black_pieces']:
                if i.row == curr_row and i.col == curr_col:
                    i.row = row
                    i.col = col
        '''
        fake_move = last_move
        '''
        if(side == 'W' or side == 'w'):
            king = b.pieces['white_pieces'][7]
            possible_moves = self.find_all_legal_moves('B', fake_move)
            if((king.return_coord()) in possible_moves):
                return True
            else:
                return False

        else:
            king = b.pieces['black_pieces'][7]
            possible_moves = self.find_all_legal_moves('W', fake_move)
            if((king.return_coord()) in possible_moves):
                return True
            else:
                return False
        '''
        return b.in_check(side, fake_move) 
      

    def move_is_legal(self, row, col, move_row, move_col, last_move):
        if(self.board[row][col] == '.'):
            return True
        else:
            piece = self.board[row][col]
            possible_moves = piece.find_legal_moves(last_move)
            return ((move_row, move_col) in possible_moves and self.pre_check(piece.side, row, col, move_row, move_col, last_move) == False)


    def find_legal_moves(self, side, last_move):
        possible_moves = set()
        if(side == 'W' or side == 'w'):
            if(self.pieces['white_pieces'][7].disabled == True):
                return set()
            
            for i in self.pieces['white_pieces']:
                for j in i.find_legal_moves(last_move):
                    if(self.pre_check(side, i.row, i.col, j[0], j[1], last_move) == False):
                        possible_moves.add(j)
        
        else:
            for i in self.pieces['black_pieces']:
                if(self.pieces['black_pieces'][7].disabled == True):
                    return set()
                for j in i.find_legal_moves(last_move):
                    if(self.pre_check(side, i.row, i.col, j[0], j[1], last_move) == False):
                        possible_moves.add(j)

        return possible_moves
    
    def find_all_legal_moves(self, side, last_move):
        possible_moves = set()
        if(side == 'W' or side == 'w'):
            for i in self.pieces['white_pieces']:
                for j in i.find_legal_moves(last_move):
                    possible_moves.add(j)
        
        else:
            for i in self.pieces['black_pieces']:
                for j in i.find_legal_moves(last_move):
                    possible_moves.add(j)

        return possible_moves


    
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
        states = {'black_left':self.black_left_castle, 'black_right':self.black_right_castle, 'white_left':self.white_left_castle, 'white_right':self.white_right_castle}
        return states
        

    def check_ally(self, row, col, side):
        if self.board[row][col] == '.':
            return False
        
        elif self.board[row][col].side != side:
            return False
        else:
            if(self.board[row][col].disabled == True):
                return False
            else:
                return True
        
    def check_enemy_king(self, row, col):
        count = 0
        #if(self.visual_board[row][col] == 'K' or self.visual_board[row][col] == 'k'):
           # count += 1

        if(row > 0 and (self.visual_board[row - 1][col] == 'K' or self.visual_board[row - 1][col] == 'k')):
            count += 1

        if(row < 7 and (self.visual_board[row + 1][col] == 'K' or self.visual_board[row + 1][col] == 'k')):
            count += 1

        if(col > 0 and (self.visual_board[row][col - 1] == 'K' or self.visual_board[row][col - 1] == 'k')):
            count += 1

        if(col < 7 and (self.visual_board[row][col + 1] == 'K' or self.visual_board[row][col + 1] == 'k')):
            count += 1

        if(row > 0 and col > 0 and (self.visual_board[row - 1][col - 1] == 'K' or self.visual_board[row - 1][col - 1] == 'k')):
            count += 1

        if(row > 0 and col < 7 and (self.visual_board[row - 1][col + 1] == 'K' or self.visual_board[row - 1][col + 1] == 'k')):
            count += 1

        if(row < 7 and col > 0 and (self.visual_board[row + 1][col - 1] == 'K' or self.visual_board[row + 1][col - 1] == 'k')):
            count += 1

        if(row < 7 and col < 7 and (self.visual_board[row + 1][col + 1] == 'K' or self.visual_board[row + 1][col + 1] == 'k')):
            count += 1

        if(count == 1):
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
            print(str(i + 1) + ' | ' + temp)
            i -= 1
        print('  | _______________')
        print('    a b c d e f g h')


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
        
        if (self.col >= 1 and self.board.check_ally(self.row, self.col-1, self.side) == False and self.board.check_enemy_king(self.row, self.col - 1) == False): 
            legal_moves.add((self.row, self.col - 1))

        if (self.col <= 6 and self.board.check_ally(self.row, self.col+1, self.side) == False and self.board.check_enemy_king(self.row, self.col + 1) == False): 
            legal_moves.add((self.row, self.col + 1))

        if (self.row >= 1 and self.board.check_ally(self.row-1, self.col, self.side) == False and self.board.check_enemy_king(self.row - 1, self.col) == False): 
            legal_moves.add((self.row - 1, self.col))

        if (self.row <= 6 and self.board.check_ally(self.row+1, self.col, self.side) == False and self.board.check_enemy_king(self.row + 1, self.col) == False): 
            legal_moves.add((self.row + 1, self.col))

        if (self.row >= 1 and self.col >= 1 and self.board.check_ally(self.row-1, self.col-1, self.side) == False and self.board.check_enemy_king(self.row - 1, self.col - 1) == False): 
            legal_moves.add((self.row - 1, self.col - 1))

        if (self.row <= 6 and self.col <= 6 and self.board.check_ally(self.row+1, self.col+1, self.side) == False and self.board.check_enemy_king(self.row + 1, self.col + 1) == False): 
            legal_moves.add((self.row + 1, self.col + 1))

        if (self.row <= 6 and self.col >= 1 and self.board.check_ally(self.row+1, self.col-1, self.side) == False and self.board.check_enemy_king(self.row + 1, self.col - 1) == False): 
            legal_moves.add((self.row + 1, self.col - 1))
            
        if (self.row >= 1 and self.col <= 6 and self.board.check_ally(self.row-1, self.col+1, self.side) == False and self.board.check_enemy_king(self.row - 1, self.col + 1) == False): 
            legal_moves.add((self.row - 1, self.col + 1))

        return legal_moves
    
    def set_piece(self):
        self.board.set_piece((self.row, self.col), self)

    def move_piece(self, row, col, last_move):
        self.board.remove_piece((self.row, self.col))
        self.board.set_piece((row, col), self)
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
        self.side = side
        self.disabled = False
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'R'
        else:
            self.icon = 'r'

    def find_legal_moves(self, last_move):
        if(self.disabled == True):
            return set()
        
        legal_moves = set()
        
        i = self.row + 1
        while (i <= 7 and self.board.board[i][self.col] == '.'):
            legal_moves.add((i, self.col))
            i += 1

        if (i <= 7 and self.board.board[i][self.col] != '.' and self.board.check_ally(i, self.col, self.side) == False):
            legal_moves.add((i, self.col))

        i = self.row - 1
        while (i >= 0 and self.board.board[i][self.col] == '.'):
            legal_moves.add((i, self.col))
            i -= 1

        if (i >= 0 and self.board.board[i][self.col] != '.' and self.board.check_ally(i, self.col, self.side) == False):
            legal_moves.add((i, self.col))

        k = self.col + 1
        while (k <= 7 and self.board.board[self.row][k] == '.'):
            legal_moves.add((self.row, k))
            k += 1

        if (k <= 7 and self.board.board[self.row][k] != '.' and self.board.check_ally(self.row, k, self.side) == False):
            legal_moves.add((self.row, k))

        k = self.col - 1
        while (k >= 0 and self.board.board[self.row][k] == '.'):
            legal_moves.add((self.row, k))
            k -= 1

        if (k >= 0 and self.board.board[self.row][k] != '.' and self.board.check_ally(self.row, k, self.side) == False):
            legal_moves.add((self.row, k))

        return legal_moves
    
    def set_piece(self):
        self.board.set_piece((self.row, self.col), self)

    def move_piece(self, row, col, last_move):
        self.board.remove_piece((self.row, self.col))
        self.board.set_piece((row, col), self)
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


class queen:
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.side = side
        self.disabled = False
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'Q'
        else:
            self.icon = 'q'

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

        i = self.row + 1
        while (i <= 7 and self.board.board[i][self.col] == '.'):
            legal_moves.add((i, self.col))
            i += 1

        if (i <= 7 and self.board.board[i][self.col] != '.' and self.board.check_ally(i, self.col, self.side) == False):
            legal_moves.add((i, self.col))

        i = self.row - 1
        while (i >= 0 and self.board.board[i][self.col] == '.'):
            legal_moves.add((i, self.col))
            i -= 1

        if (i >= 0 and self.board.board[i][self.col] != '.' and self.board.check_ally(i, self.col, self.side) == False):
            legal_moves.add((i, self.col))

        k = self.col + 1
        while (k <= 7 and self.board.board[self.row][k] == '.'):
            legal_moves.add((self.row, k))
            k += 1

        if (k <= 7 and self.board.board[self.row][k] != '.' and self.board.check_ally(self.row, k, self.side) == False):
            legal_moves.add((self.row, k))

        k = self.col - 1
        while (k >= 0 and self.board.board[self.row][k] == '.'):
            legal_moves.add((self.row, k))
            k -= 1

        if (k >= 0 and self.board.board[self.row][k] != '.' and self.board.check_ally(self.row, k, self.side) == False):
            legal_moves.add((self.row, k))

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

    P1 = pawn(board, 1, 0, 'W')
    P2 = pawn(board, 1, 1, 'W')
    P3 = pawn(board, 1, 2, 'W')
    P4 = pawn(board, 1, 3, 'W')
    P5 = pawn(board, 1, 4, 'W')
    P6 = pawn(board, 1, 5, 'W')
    P7 = pawn(board, 1, 6, 'W')
    P8 = pawn(board, 1, 7, 'W')


    #black pieces

    r1 = rook(board, 7, 0, 'B')
    r2 = rook(board, 7, 7, 'B')

    n1 = knight(board, 7, 1, 'B')
    n2 = knight(board, 7, 6, 'B')

    b1 = bishop(board, 7, 2, 'B')
    b2 = bishop(board, 7, 5, 'B')

    q = queen(board, 7, 3, 'B')

    k = king(board, 7, 4, 'B')

    p1 = pawn(board, 6, 0, 'B')
    p2 = pawn(board, 6, 1, 'B')
    p3 = pawn(board, 6, 2, 'B')
    p4 = pawn(board, 6, 3, 'B')
    p5 = pawn(board, 6, 4, 'B')
    p6 = pawn(board, 6, 5, 'B')
    p7 = pawn(board, 6, 6, 'B')
    p8 = pawn(board, 6, 7, 'B')

    #piece dictionary

    pieces.update({'white_pieces' : [R1, R2, N1, N2, B1, B2, Q, K, P1, P2, P3, P4, P5, P6, P7, P8]})
    pieces.update({'black_pieces' : [r1, r2, n1, n2, b1, b2, q, k, p1, p2, p3, p4, p5, p6, p7, p8]})

    #set_pieces

    for i in pieces['white_pieces']:
        i.set_piece()

    for k in pieces['black_pieces']:
        k.set_piece()

    return pieces


####################################################################################
def convert_notation(coord):
    match coord[1]:
        case 0:
            col = 'a'
        case 1:
            col = 'b'
        case 2:
            col = 'c'
        case 3:
            col = 'd'
        case 4:
            col = 'e'
        case 5:
            col = 'f'
        case 6:
            col = 'g'
        case 7:
            col = 'h'
    return col + str(coord[0]+1)

def legal_move(board, side, curr_row, curr_col, row, col, last_move):
    if(board.board[curr_row][curr_col] == '.'):
        return False
    elif(board.board[curr_row][curr_col].side != 'W'):
        return False
    else:
        return board.move_is_legal(curr_row, curr_col, row, col, last_move)
    
def check_valid(chatgpt, board, begin_coord, end_coord, last_move):
    if(legal_move(board, 'W', begin_coord[0], begin_coord[1], end_coord[0], end_coord[1], last_move) == False):
        return False
    else:
        if(board.board[begin_coord[0]][begin_coord[1]] != '.'):
            if(b.board[end_coord[0]][end_coord[1]] != '.'):
                b.board[end_coord[0]][end_coord[1]].disabled = True
        board.board[begin_coord[0]][begin_coord[1]].move_piece(end_coord[0], end_coord[1], last_move)
        if(board.check_mate('B', last_move) == True):        
            return {"result": "white won", "previous": begin_coord, "next": end_coord, "response": "Well played! You Won!"}

        message = convert_notation(begin_coord) + " to " + convert_notation(end_coord)
        move = ask_gpt(chatgpt, message, board, '', 'black')
        result = "no win"
        if(b.board[move[2][0]][move[2][1]] != '.'):
            if(b.board[move[3][0]][move[3][1]] != '.'):
                b.board[move[3][0]][move[3][1]].disabled = True
            if(b.pieces['black_pieces'][7].disabled == True):
                result = "black surrenders"
            else:
                b.board[move[2][0]][move[2][1]].move_piece(move[3][0], move[3][1], last_move)
        
        
        if(b.check_mate('W', last_move) == True):
            result = "black won"
        
        return {"result": result, "previous": move[2], "next": move[3], "response": move[4]}




####################################################################################
if __name__ == '__main__':  
    client = OpenAI()

    m = ''
    b = board()
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}
    print(check_valid(client, b, (1, 4), (3, 4), last_move))
    b.print_board()
    '''
    #i = 0
    #print(get_coords("e4"))
    while(True):
        print("white move: ")
        move = ask_gpt(client, m, b, side = "white")
        m = move[0] + ' to ' + move[1]
        print("piece: ", b.visual_board[move[2][0]][move[2][1]])
        print("move is legal: ", b.move_is_legal(move[2][0], move[2][1], move[3][0], move[3][1], last_move))
        if(b.board[move[2][0]][move[2][1]] != "."):
            if(b.board[move[3][0]][move[3][1]] != '.'):
                b.board[move[3][0]][move[3][1]].disabled = True
            if(b.pieces['white_pieces'][7].disabled == True):
                print("White surrenders!")
                break
            b.board[move[2][0]][move[2][1]].move_piece(move[3][0], move[3][1], last_move)

        legal_moves = b.find_legal_moves("b", last_move)
        
        print("legal_moves: ", legal_moves)
        print("queen legal moves: ", b.pieces['white_pieces'][6].find_legal_moves(last_move))
        b.print_board()
        if(b.check_mate('B', last_move) == True): #or b.pieces['black_pieces'][7].disabled == True):
            print(b.pieces['black_pieces'][7].find_legal_moves(last_move))
            for i in b.pieces['black_pieces']:
                print(i.icon, i.find_legal_moves(last_move))
            print("White won!")
            break
        
        print("black move: ")
        move = ask_gpt(client, m, b, side = "black")
        m = move[0] + ' to ' + move[1]
        print("piece: ", b.visual_board[move[2][0]][move[2][1]])
        print("move is legal: ", b.move_is_legal(move[2][0], move[2][1], move[3][0], move[3][1], last_move))
        if(b.board[move[2][0]][move[2][1]] != "."):
            if(b.board[move[3][0]][move[3][1]] != '.'):
                b.board[move[3][0]][move[3][1]].disabled = True
            if(b.pieces['black_pieces'][7].disabled == True):
                print("Black surrenders!")
                break
            b.board[move[2][0]][move[2][1]].move_piece(move[3][0], move[3][1], last_move)

        legal_moves = b.find_legal_moves("w", last_move)
        
        print("legal_moves: ", legal_moves)
        print("queen legal moves: ", b.pieces['black_pieces'][6].find_legal_moves(last_move))
        b.print_board()
        if(b.check_mate('W', last_move) == True): #or b.pieces['white_pieces'][7].disabled == True):
            print(b.pieces['white_pieces'][7].find_legal_moves(last_move))
            for i in b.pieces['white_pieces']:
                print(i.icon, i.find_legal_moves(last_move))
            print("Black won!")
            break
    '''










    #test1 = get_web_notation("Nc3")
    #test2 = get_gpt_notation(test1)
    #print(test1)
    #print(test2)

    #print(move("e2:e4", client, board, m))
    '''
    b = board()
    p = b.return_pieces()
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}

    print(b.in_check('W', last_move))
    b.print_board()

    print(b.find_all_legal_moves('b', last_move))

    print(b.pieces['black_pieces'][12].find_legal_moves(last_move))

    print(b.pre_check('W', 0, 4, 2, 4, last_move))

    p['black_pieces'][3].move_piece(5, 5, last_move)
    
    b.print_board()

    print(b.find_all_legal_moves('b', last_move))

    p['black_pieces'][3].move_piece(7, 6, last_move)

    b.print_board()

    print(b.find_all_legal_moves('b', last_move))

    '''
    


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
#import os
import time
import copy
#import chess
from openai import OpenAI
#from dotenv import load_dotenv
#load_dotenv()

#AI prompt: make a move as white based on this chess position, give the move notation in the format of (original square, new square) without additional text

def ask_gpt(client, move_str, board, error_str = "", side = "black"):
    #try:
    completion = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {"role": "system", "content": "You are a chess master that will make good chess moves"},
            {"role": "user", "content":  error_str + "last move was " + move_str + ", based on the game moves given, make one chess move on " + side + " side, return the move in the format of tuple(starting coordinate, end coordinate) without additional texts"}
        ]
    )
    
    reply = completion.choices[0].message.content

    response = reply
    response = response.replace("(", "")
    response = response.replace(")", "")
    response = response.replace("'", "")
    response = response.replace("\"", "")
    '''
    if ('.' in reply):
        temp = reply.split('.')
        response = temp[-1]
    
    if (' ' in reply):
        temp = reply.split(' ')
        response = temp[-1]

    if (len(response) > 7 or response == None or ('-' in response and 'O' in response)):
        print(len(response))
        ask_gpt(client, move_list, board, side = side)
    '''
    if(len(response) > 10 or "," not in response):
        print(response)
        time.sleep(5)
        return ask_gpt(client, move_str, board, "only return the tuple(starting coordinate, end coordinate) ")
    else:
        try:
            #board.parse_san(response)
            #print(response)
            #move_list.append(response)
            #return response
            
            #move = response.replace("(", "")
            #move = move.replace(")", "")
            move = response.split(", ")
            start = move[0]
            print("start: ", start)
            end = move[1]
            print("end: ", end)
            return [start, end, get_coords(start), get_coords(end), reply]
            #start_coord = get_coords(start)
            #end_coord = get_coords(end)
            #print("return: ", start, end, start_coord, end_coord)
            
        
        except:
            print(response)
            time.sleep(5)
            return ask_gpt(client, move_str, board, "only return the tuple(starting coordinate, end coordinate) ")
            #print("ChatGPT made an illegal move")
            #error_str = response + " was an illegal move! "
            #ask_gpt(client, move_list, board, error_str, side)
    '''   
    except:
        print("Waiting for ChatGPT...")
        time.sleep(5)
        return ask_gpt(client, move_list, board, "only return the tuple(starting coordinate, end coordinate) ")
    '''

def get_coords(notation):
    print("get_coords: ", notation)
    match notation[0]:
        case 'a':
            col = 0
        case 'b':
            col = 1
        case 'c':
            col = 2
        case 'd':
            col = 3
        case 'e':
            col = 4
        case 'f':
            col = 5
        case 'g':
            col = 6
        case 'h':
            col = 7
    
    return (int(notation[1]) - 1, col)
    
'''
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
'''
####################################################################################
class board:
    def __init__(self):
        self.visual_board = [
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.']
                     ]
        
        self.board = [
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.']
                     ]
        
        self.board_states = []
        self.num_moves = 0

        self.pieces = set_board(self)

        self.black_left_castle = True
        self.black_right_castle = True
        self.white_left_castle = True
        self.white_right_castle = True


    def return_pieces(self):
        return self.pieces
    
    
    def check_mate(self, side, last_move):
        if(self.in_check(side, last_move) == False):
            return False
        else:
            if(side == 'W' or side == 'w'):
                for i in b.pieces['black_pieces']:
                    for j in i.find_legal_moves(last_move):
                        if(self.pre_check(side, i.row, i.col, j[0], j[1], last_move) == False):
                            return False
                return True
            elif(side == 'B' or side == 'b'):
                for i in b.pieces['white_pieces']:
                    for j in i.find_legal_moves(last_move):
                        if(self.pre_check(side, i.row, i.col, j[0], j[1], last_move) == False):
                            return False
                return True
    
    def in_check(self, side, last_move):
        if(side == 'W' or side == 'w'):
            king = self.pieces['white_pieces'][7]
            possible_moves = self.find_all_legal_moves('B', last_move)
            if((king.return_coord()) in possible_moves):
                print("In check: ", king.return_coord())
                return True
            else:
                return False

        else:
            king = self.pieces['black_pieces'][7]
            possible_moves = self.find_all_legal_moves('W', last_move)
            if((king.return_coord()) in possible_moves):
                return True
            else:
                return False
        
    def pre_check(self, side, curr_row, curr_col, row, col, last_move):        
        b = board()
        
        b.board = copy.deepcopy(self.board)
        b.visual_board = copy.deepcopy(self.visual_board)
        b.pieces = copy.deepcopy(self.pieces)

        for i in b.pieces['white_pieces']:
            i.board = b
        
        for i in b.pieces['black_pieces']:
            i.board = b

        for i in b.board:
            for j in i:
                if(j != '.'):
                    j.board = b
        

        piece1 = b.board[curr_row][curr_col]
        piece2 = b.board[row][col]

        b.remove_piece((curr_row, curr_col))
        if(piece1 != '.'):
            #b.set_piece((row, col), piece1)
            if(piece2 != '.'):
                b.remove_piece((row, col))
            piece1.move_piece(row, col, last_move)

        if(piece2 != '.'):
            piece2.disable = True

        '''
        if(side == 'W'):
            for i in b.pieces['white_pieces']:
                if i.row == curr_row and i.col == curr_col:
                    i.row = row
                    i.col = col
        else:
            for i in b.pieces['black_pieces']:
                if i.row == curr_row and i.col == curr_col:
                    i.row = row
                    i.col = col
        '''
        fake_move = last_move
        '''
        if(side == 'W' or side == 'w'):
            king = b.pieces['white_pieces'][7]
            possible_moves = self.find_all_legal_moves('B', fake_move)
            if((king.return_coord()) in possible_moves):
                return True
            else:
                return False

        else:
            king = b.pieces['black_pieces'][7]
            possible_moves = self.find_all_legal_moves('W', fake_move)
            if((king.return_coord()) in possible_moves):
                return True
            else:
                return False
        '''
        return b.in_check(side, fake_move) 
      

    def move_is_legal(self, row, col, move_row, move_col, last_move):
        if(self.board[row][col] == '.'):
            return True
        else:
            piece = self.board[row][col]
            possible_moves = piece.find_legal_moves(last_move)
            return ((move_row, move_col) in possible_moves and self.pre_check(piece.side, row, col, move_row, move_col, last_move) == False)


    def find_legal_moves(self, side, last_move):
        possible_moves = set()
        if(side == 'W' or side == 'w'):
            if(self.pieces['white_pieces'][7].disabled == True):
                return set()
            
            for i in self.pieces['white_pieces']:
                for j in i.find_legal_moves(last_move):
                    if(self.pre_check(side, i.row, i.col, j[0], j[1], last_move) == False):
                        possible_moves.add(j)
        
        else:
            for i in self.pieces['black_pieces']:
                if(self.pieces['black_pieces'][7].disabled == True):
                    return set()
                for j in i.find_legal_moves(last_move):
                    if(self.pre_check(side, i.row, i.col, j[0], j[1], last_move) == False):
                        possible_moves.add(j)

        return possible_moves
    
    def find_all_legal_moves(self, side, last_move):
        possible_moves = set()
        if(side == 'W' or side == 'w'):
            for i in self.pieces['white_pieces']:
                for j in i.find_legal_moves(last_move):
                    possible_moves.add(j)
        
        else:
            for i in self.pieces['black_pieces']:
                for j in i.find_legal_moves(last_move):
                    possible_moves.add(j)

        return possible_moves


    
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
        states = {'black_left':self.black_left_castle, 'black_right':self.black_right_castle, 'white_left':self.white_left_castle, 'white_right':self.white_right_castle}
        return states
        

    def check_ally(self, row, col, side):
        if self.board[row][col] == '.':
            return False
        
        elif self.board[row][col].side != side:
            return False
        else:
            if(self.board[row][col].disabled == True):
                return False
            else:
                return True
        
    def check_enemy_king(self, row, col):
        count = 0
        #if(self.visual_board[row][col] == 'K' or self.visual_board[row][col] == 'k'):
           # count += 1

        if(row > 0 and (self.visual_board[row - 1][col] == 'K' or self.visual_board[row - 1][col] == 'k')):
            count += 1

        if(row < 7 and (self.visual_board[row + 1][col] == 'K' or self.visual_board[row + 1][col] == 'k')):
            count += 1

        if(col > 0 and (self.visual_board[row][col - 1] == 'K' or self.visual_board[row][col - 1] == 'k')):
            count += 1

        if(col < 7 and (self.visual_board[row][col + 1] == 'K' or self.visual_board[row][col + 1] == 'k')):
            count += 1

        if(row > 0 and col > 0 and (self.visual_board[row - 1][col - 1] == 'K' or self.visual_board[row - 1][col - 1] == 'k')):
            count += 1

        if(row > 0 and col < 7 and (self.visual_board[row - 1][col + 1] == 'K' or self.visual_board[row - 1][col + 1] == 'k')):
            count += 1

        if(row < 7 and col > 0 and (self.visual_board[row + 1][col - 1] == 'K' or self.visual_board[row + 1][col - 1] == 'k')):
            count += 1

        if(row < 7 and col < 7 and (self.visual_board[row + 1][col + 1] == 'K' or self.visual_board[row + 1][col + 1] == 'k')):
            count += 1

        if(count == 1):
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
            print(str(i + 1) + ' | ' + temp)
            i -= 1
        print('  | _______________')
        print('    a b c d e f g h')


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
        
        if (self.col >= 1 and self.board.check_ally(self.row, self.col-1, self.side) == False and self.board.check_enemy_king(self.row, self.col - 1) == False): 
            legal_moves.add((self.row, self.col - 1))

        if (self.col <= 6 and self.board.check_ally(self.row, self.col+1, self.side) == False and self.board.check_enemy_king(self.row, self.col + 1) == False): 
            legal_moves.add((self.row, self.col + 1))

        if (self.row >= 1 and self.board.check_ally(self.row-1, self.col, self.side) == False and self.board.check_enemy_king(self.row - 1, self.col) == False): 
            legal_moves.add((self.row - 1, self.col))

        if (self.row <= 6 and self.board.check_ally(self.row+1, self.col, self.side) == False and self.board.check_enemy_king(self.row + 1, self.col) == False): 
            legal_moves.add((self.row + 1, self.col))

        if (self.row >= 1 and self.col >= 1 and self.board.check_ally(self.row-1, self.col-1, self.side) == False and self.board.check_enemy_king(self.row - 1, self.col - 1) == False): 
            legal_moves.add((self.row - 1, self.col - 1))

        if (self.row <= 6 and self.col <= 6 and self.board.check_ally(self.row+1, self.col+1, self.side) == False and self.board.check_enemy_king(self.row + 1, self.col + 1) == False): 
            legal_moves.add((self.row + 1, self.col + 1))

        if (self.row <= 6 and self.col >= 1 and self.board.check_ally(self.row+1, self.col-1, self.side) == False and self.board.check_enemy_king(self.row + 1, self.col - 1) == False): 
            legal_moves.add((self.row + 1, self.col - 1))
            
        if (self.row >= 1 and self.col <= 6 and self.board.check_ally(self.row-1, self.col+1, self.side) == False and self.board.check_enemy_king(self.row - 1, self.col + 1) == False): 
            legal_moves.add((self.row - 1, self.col + 1))

        return legal_moves
    
    def set_piece(self):
        self.board.set_piece((self.row, self.col), self)

    def move_piece(self, row, col, last_move):
        self.board.remove_piece((self.row, self.col))
        self.board.set_piece((row, col), self)
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
        self.side = side
        self.disabled = False
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'R'
        else:
            self.icon = 'r'

    def find_legal_moves(self, last_move):
        if(self.disabled == True):
            return set()
        
        legal_moves = set()
        
        i = self.row + 1
        while (i <= 7 and self.board.board[i][self.col] == '.'):
            legal_moves.add((i, self.col))
            i += 1

        if (i <= 7 and self.board.board[i][self.col] != '.' and self.board.check_ally(i, self.col, self.side) == False):
            legal_moves.add((i, self.col))

        i = self.row - 1
        while (i >= 0 and self.board.board[i][self.col] == '.'):
            legal_moves.add((i, self.col))
            i -= 1

        if (i >= 0 and self.board.board[i][self.col] != '.' and self.board.check_ally(i, self.col, self.side) == False):
            legal_moves.add((i, self.col))

        k = self.col + 1
        while (k <= 7 and self.board.board[self.row][k] == '.'):
            legal_moves.add((self.row, k))
            k += 1

        if (k <= 7 and self.board.board[self.row][k] != '.' and self.board.check_ally(self.row, k, self.side) == False):
            legal_moves.add((self.row, k))

        k = self.col - 1
        while (k >= 0 and self.board.board[self.row][k] == '.'):
            legal_moves.add((self.row, k))
            k -= 1

        if (k >= 0 and self.board.board[self.row][k] != '.' and self.board.check_ally(self.row, k, self.side) == False):
            legal_moves.add((self.row, k))

        return legal_moves
    
    def set_piece(self):
        self.board.set_piece((self.row, self.col), self)

    def move_piece(self, row, col, last_move):
        self.board.remove_piece((self.row, self.col))
        self.board.set_piece((row, col), self)
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


class queen:
    def __init__(self, board, row, col, side):
        self.board = board
        self.row = row
        self.col = col
        self.side = side
        self.disabled = False
        if (self.side == 'W' or self.side == 'w'):
            self.icon = 'Q'
        else:
            self.icon = 'q'

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

        i = self.row + 1
        while (i <= 7 and self.board.board[i][self.col] == '.'):
            legal_moves.add((i, self.col))
            i += 1

        if (i <= 7 and self.board.board[i][self.col] != '.' and self.board.check_ally(i, self.col, self.side) == False):
            legal_moves.add((i, self.col))

        i = self.row - 1
        while (i >= 0 and self.board.board[i][self.col] == '.'):
            legal_moves.add((i, self.col))
            i -= 1

        if (i >= 0 and self.board.board[i][self.col] != '.' and self.board.check_ally(i, self.col, self.side) == False):
            legal_moves.add((i, self.col))

        k = self.col + 1
        while (k <= 7 and self.board.board[self.row][k] == '.'):
            legal_moves.add((self.row, k))
            k += 1

        if (k <= 7 and self.board.board[self.row][k] != '.' and self.board.check_ally(self.row, k, self.side) == False):
            legal_moves.add((self.row, k))

        k = self.col - 1
        while (k >= 0 and self.board.board[self.row][k] == '.'):
            legal_moves.add((self.row, k))
            k -= 1

        if (k >= 0 and self.board.board[self.row][k] != '.' and self.board.check_ally(self.row, k, self.side) == False):
            legal_moves.add((self.row, k))

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

    P1 = pawn(board, 1, 0, 'W')
    P2 = pawn(board, 1, 1, 'W')
    P3 = pawn(board, 1, 2, 'W')
    P4 = pawn(board, 1, 3, 'W')
    P5 = pawn(board, 1, 4, 'W')
    P6 = pawn(board, 1, 5, 'W')
    P7 = pawn(board, 1, 6, 'W')
    P8 = pawn(board, 1, 7, 'W')


    #black pieces

    r1 = rook(board, 7, 0, 'B')
    r2 = rook(board, 7, 7, 'B')

    n1 = knight(board, 7, 1, 'B')
    n2 = knight(board, 7, 6, 'B')

    b1 = bishop(board, 7, 2, 'B')
    b2 = bishop(board, 7, 5, 'B')

    q = queen(board, 7, 3, 'B')

    k = king(board, 7, 4, 'B')

    p1 = pawn(board, 6, 0, 'B')
    p2 = pawn(board, 6, 1, 'B')
    p3 = pawn(board, 6, 2, 'B')
    p4 = pawn(board, 6, 3, 'B')
    p5 = pawn(board, 6, 4, 'B')
    p6 = pawn(board, 6, 5, 'B')
    p7 = pawn(board, 6, 6, 'B')
    p8 = pawn(board, 6, 7, 'B')

    #piece dictionary

    pieces.update({'white_pieces' : [R1, R2, N1, N2, B1, B2, Q, K, P1, P2, P3, P4, P5, P6, P7, P8]})
    pieces.update({'black_pieces' : [r1, r2, n1, n2, b1, b2, q, k, p1, p2, p3, p4, p5, p6, p7, p8]})

    #set_pieces

    for i in pieces['white_pieces']:
        i.set_piece()

    for k in pieces['black_pieces']:
        k.set_piece()

    return pieces


####################################################################################
def convert_notation(coord):
    match coord[1]:
        case 0:
            col = 'a'
        case 1:
            col = 'b'
        case 2:
            col = 'c'
        case 3:
            col = 'd'
        case 4:
            col = 'e'
        case 5:
            col = 'f'
        case 6:
            col = 'g'
        case 7:
            col = 'h'
    return col + str(coord[0]+1)

def legal_move(board, side, curr_row, curr_col, row, col, last_move):
    if(board.board[curr_row][curr_col] == '.'):
        return False
    elif(board.board[curr_row][curr_col].side != 'W'):
        return False
    else:
        return board.move_is_legal(curr_row, curr_col, row, col, last_move)
    
def check_valid(chatgpt, board, begin_coord, end_coord, last_move):
    if(legal_move(board, 'W', begin_coord[0], begin_coord[1], end_coord[0], end_coord[1], last_move) == False):
        return False
    else:
        if(board.board[begin_coord[0]][begin_coord[1]] != '.'):
            if(b.board[end_coord[0]][end_coord[1]] != '.'):
                b.board[end_coord[0]][end_coord[1]].disabled = True
        board.board[begin_coord[0]][begin_coord[1]].move_piece(end_coord[0], end_coord[1], last_move)
        if(board.check_mate('B', last_move) == True):        
            return {"result": "white won", "previous": begin_coord, "next": end_coord, "response": "Well played! You Won!"}

        message = convert_notation(begin_coord) + " to " + convert_notation(end_coord)
        move = ask_gpt(chatgpt, message, board, '', 'black')
        result = "no win"
        if(b.board[move[2][0]][move[2][1]] != '.'):
            if(b.board[move[3][0]][move[3][1]] != '.'):
                b.board[move[3][0]][move[3][1]].disabled = True
            if(b.pieces['black_pieces'][7].disabled == True):
                result = "black surrenders"
            else:
                b.board[move[2][0]][move[2][1]].move_piece(move[3][0], move[3][1], last_move)
        
        
        if(b.check_mate('W', last_move) == True):
            result = "black won"
        
        return {"result": result, "previous": move[2], "next": move[3], "response": move[4]}




####################################################################################
if __name__ == '__main__':  
    client = OpenAI()

    m = ''
    b = board()
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}
    print(check_valid(client, b, (1, 4), (3, 4), last_move))
    b.print_board()
    '''
    #i = 0
    #print(get_coords("e4"))
    while(True):
        print("white move: ")
        move = ask_gpt(client, m, b, side = "white")
        m = move[0] + ' to ' + move[1]
        print("piece: ", b.visual_board[move[2][0]][move[2][1]])
        print("move is legal: ", b.move_is_legal(move[2][0], move[2][1], move[3][0], move[3][1], last_move))
        if(b.board[move[2][0]][move[2][1]] != "."):
            if(b.board[move[3][0]][move[3][1]] != '.'):
                b.board[move[3][0]][move[3][1]].disabled = True
            if(b.pieces['white_pieces'][7].disabled == True):
                print("White surrenders!")
                break
            b.board[move[2][0]][move[2][1]].move_piece(move[3][0], move[3][1], last_move)

        legal_moves = b.find_legal_moves("b", last_move)
        
        print("legal_moves: ", legal_moves)
        print("queen legal moves: ", b.pieces['white_pieces'][6].find_legal_moves(last_move))
        b.print_board()
        if(b.check_mate('B', last_move) == True): #or b.pieces['black_pieces'][7].disabled == True):
            print(b.pieces['black_pieces'][7].find_legal_moves(last_move))
            for i in b.pieces['black_pieces']:
                print(i.icon, i.find_legal_moves(last_move))
            print("White won!")
            break
        
        print("black move: ")
        move = ask_gpt(client, m, b, side = "black")
        m = move[0] + ' to ' + move[1]
        print("piece: ", b.visual_board[move[2][0]][move[2][1]])
        print("move is legal: ", b.move_is_legal(move[2][0], move[2][1], move[3][0], move[3][1], last_move))
        if(b.board[move[2][0]][move[2][1]] != "."):
            if(b.board[move[3][0]][move[3][1]] != '.'):
                b.board[move[3][0]][move[3][1]].disabled = True
            if(b.pieces['black_pieces'][7].disabled == True):
                print("Black surrenders!")
                break
            b.board[move[2][0]][move[2][1]].move_piece(move[3][0], move[3][1], last_move)

        legal_moves = b.find_legal_moves("w", last_move)
        
        print("legal_moves: ", legal_moves)
        print("queen legal moves: ", b.pieces['black_pieces'][6].find_legal_moves(last_move))
        b.print_board()
        if(b.check_mate('W', last_move) == True): #or b.pieces['white_pieces'][7].disabled == True):
            print(b.pieces['white_pieces'][7].find_legal_moves(last_move))
            for i in b.pieces['white_pieces']:
                print(i.icon, i.find_legal_moves(last_move))
            print("Black won!")
            break
    '''










    #test1 = get_web_notation("Nc3")
    #test2 = get_gpt_notation(test1)
    #print(test1)
    #print(test2)

    #print(move("e2:e4", client, board, m))
    '''
    b = board()
    p = b.return_pieces()
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}

    print(b.in_check('W', last_move))
    b.print_board()

    print(b.find_all_legal_moves('b', last_move))

    print(b.pieces['black_pieces'][12].find_legal_moves(last_move))

    print(b.pre_check('W', 0, 4, 2, 4, last_move))

    p['black_pieces'][3].move_piece(5, 5, last_move)
    
    b.print_board()

    print(b.find_all_legal_moves('b', last_move))

    p['black_pieces'][3].move_piece(7, 6, last_move)

    b.print_board()

    print(b.find_all_legal_moves('b', last_move))

    '''
    


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

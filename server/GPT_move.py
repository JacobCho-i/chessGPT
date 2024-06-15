#import os
import time
import copy
#import chess
from openai import OpenAI
from dotenv import load_dotenv
from queen import queen
from knight import knight
from pawn import pawn
from rook import rook
from king import king
from bishop import bishop
load_dotenv()

#AI prompt: make a move as white based on this chess position, give the move notation in the format of (original square, new square) without additional text

def ask_gpt(client, move_str, board, error_str = "", side = "black"):
    #try:
    completion = client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {"role": "system", "content": "You are a chess master that will make good chess moves"},
            {"role": "user", "content":  error_str + "last move was " + move_str + ", based on the game moves given, make one chess move on " + side + " side, return the move in the format of tuple in a format of (starting coordinate, end coordinate) without additional texts. Some example response is (e4, f4), (a1, a3), follow this format"}
        ]
    )
    
    reply = completion.choices[0].message.content

    response = reply
    response = response.replace("(", "")
    response = response.replace(")", "")
    response = response.replace("'", "")
    response = response.replace("\"", "")
    if(len(response) > 10 or "," not in response):
        print(response)
        return ask_gpt(client, move_str, board, "only return the tuple(starting coordinate, end coordinate) ")
    else:
        try:
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
            return ask_gpt(client, move_str, board, "only return the tuple(starting coordinate, end coordinate) ")

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

        self.disabled_white_pieces = []
        self.disabled_black_pieces = []


    def return_pieces(self):
        return self.pieces
    
    
    def check_mate(self, side, last_move):
        if(self.in_check(side, last_move) == False):
            return False
        else:
            if(side == 'W' or side == 'w'):
                for i in self.pieces['black_pieces']:
                    for j in i.find_legal_moves(last_move):
                        if(self.pre_check(side, i.row, i.col, j[0], j[1], last_move) == False):
                            return False
                return True
            elif(side == 'B' or side == 'b'):
                for i in self.pieces['white_pieces']:
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
                print("In check: ", king.return_coord())
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

        fake_move = last_move

        return b.in_check(side, fake_move) 
      

    def move_is_legal(self, row, col, move_row, move_col, last_move):
        if(self.board[row][col] == '.'):
            return True
        else:
            piece = self.board[row][col]
            possible_moves = piece.find_legal_moves(last_move)
            return (move_row, move_col) in possible_moves#((move_row, move_col) in possible_moves and self.pre_check(piece.side, row, col, move_row, move_col, last_move) == False)


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

def king_removed(board, side):
    board.print_board()
    if(side == 'B' or side == 'b'):
        icon = 'k'
    else:
        icon = 'K'
    for i in board.visual_board:
        for j in i:
            if(j == icon):
                return False
    return True

def legal_move(board, side, curr_row, curr_col, row, col, last_move):
    if(board.board[curr_row][curr_col] == '.'):
        return False
    elif(board.board[curr_row][curr_col].side != 'W'):
        return False
    elif((curr_row == 0 and curr_col == 4) and (board.visual_board[curr_row][curr_col] == 'K') and (row == 0)):
        if(col == 2):
            return (board.visual_board[0][1] == '.' and board.visual_board[0][2] == '.' and board.visual_board[0][3] == '.' and board.move_is_legal(curr_row, curr_col, row, col, last_move))
        elif(col == 6):
            return (board.visual_board[0][5] == '.' and board.visual_board[0][6] == '.' and board.move_is_legal(curr_row, curr_col, row, col, last_move))
    else:
        return board.move_is_legal(curr_row, curr_col, row, col, last_move)
    
def check_valid(chatgpt, board, begin_coord, end_coord, last_move):
    if(legal_move(board, 'W', begin_coord[0], begin_coord[1], end_coord[0], end_coord[1], last_move) == False):
        return False
    else:
        if(board.board[begin_coord[0]][begin_coord[1]] != '.'):
            if(board.board[end_coord[0]][end_coord[1]] != '.'):
                board.board[end_coord[0]][end_coord[1]].disabled = True
                if(board.board[end_coord[0]][end_coord[1]].side == 'W' or board.board[end_coord[0]][end_coord[1]].side == 'w'):
                    board.disabled_white_pieces.append(board.board[end_coord[0]][end_coord[1]].icon)
                elif(board.board[end_coord[0]][end_coord[1]].side == 'B' or board.board[end_coord[0]][end_coord[1]].side == 'b'):
                    board.disabled_black_pieces.append(board.board[end_coord[0]][end_coord[1]].icon)

        board.board[begin_coord[0]][begin_coord[1]].move_piece(end_coord[0], end_coord[1], last_move)
        board.print_board()

        if(board.pieces['black_pieces'][7].disabled == True or king_removed(board, 'B') == True):
            disabled_white_pieces = []
            newboard = copy.deepcopy(board.visual_board)
            newboard[0], newboard[1], newboard[2], newboard[3], newboard[4], newboard[5], newboard[6], newboard[7] = newboard[7], newboard[6], newboard[5], newboard[4], newboard[3], newboard[2], newboard[1], newboard[0]
            return {"result": "white won", "previous": begin_coord, "next": end_coord, "response": "Good Game!", "board": newboard, "disabled_white_pieces": board.disabled_white_pieces, "disabled_black_pieces": board.disabled_black_pieces}
        
        elif(board.pieces['white_pieces'][7].disabled == True or king_removed(board, 'W') == True):
            newboard = copy.deepcopy(board.visual_board)
            newboard[0], newboard[1], newboard[2], newboard[3], newboard[4], newboard[5], newboard[6], newboard[7] = newboard[7], newboard[6], newboard[5], newboard[4], newboard[3], newboard[2], newboard[1], newboard[0]
            return {"result": "black won", "previous": begin_coord, "next": end_coord, "response": "Good Game!", "board": newboard, "disabled_white_pieces": board.disabled_white_pieces, "disabled_black_pieces": board.disabled_black_pieces}


        message = convert_notation(begin_coord) + " to " + convert_notation(end_coord)
        move = ask_gpt(chatgpt, message, board, '', 'black')
        result = "no win"
        if(board.board[move[2][0]][move[2][1]] != '.'):
            if(board.board[move[3][0]][move[3][1]] != '.'):
                board.board[move[3][0]][move[3][1]].disabled = True
                if(board.board[end_coord[0]][end_coord[1]].side == 'W' or board.board[end_coord[0]][end_coord[1]].side == 'w'):
                    board.disabled_white_pieces.append(board.board[end_coord[0]][end_coord[1]].icon)
                elif(board.board[end_coord[0]][end_coord[1]].side == 'B' or board.board[end_coord[0]][end_coord[1]].side == 'b'):
                    board.disabled_black_pieces.append(board.board[end_coord[0]][end_coord[1]].icon)

            board.board[move[2][0]][move[2][1]].move_piece(move[3][0], move[3][1], last_move)
        
        else:
            if(board.board[move[3][0]][move[3][1]] != '.'):
                board.board[move[3][0]][move[3][1]].disabled == True
                if(board.board[end_coord[0]][end_coord[1]].side == 'W' or board.board[end_coord[0]][end_coord[1]].side == 'w'):
                    board.disabled_white_pieces.append(board.board[end_coord[0]][end_coord[1]].icon)
                elif(board.board[end_coord[0]][end_coord[1]].side == 'B' or board.board[end_coord[0]][end_coord[1]].side == 'b'):
                    board.disabled_black_pieces.append(board.board[end_coord[0]][end_coord[1]].icon)
                board.remove_piece((move[3][0], move[3][1]))
            if(move[3][0] != 7):
                p = pawn(board, move[3][0], move[3][1], 'B')
            else:
                match move[3][1]:
                    case 0 | 7:
                        p = rook(board, move[3][0], move[3][1], 'B')
                    case 1 | 6:
                        p = knight(board, move[3][0], move[3][1], 'B')
                    case 2 | 5: 
                        p = bishop(board, move[3][0], move[3][1], 'B')
                    case 3:
                        p = queen(board, move[3][0], move[3][1], 'B')
                    case 4:
                        p = king(board, move[3][0], move[3][1], 'B')

            board.pieces['black_pieces'].append(p)
            board.set_piece((move[3][0], move[3][1]), p)
            #board.board[move[3][0]][move[3][1]].move_piece(move[3][0], move[3][1], last_move)

        board.print_board()
        
        if(board.pieces['black_pieces'][7].disabled == True or king_removed(board, 'B') == True):
            result = "white won"
        elif(board.pieces['white_pieces'][7].disabled == True or king_removed(board, 'W') == True):
            result = "black won"
        else:
            result = "no win"

        newboard = copy.deepcopy(board.visual_board)
        newboard[move[2][0]][move[2][1]] = '!'
        newboard[0], newboard[1], newboard[2], newboard[3], newboard[4], newboard[5], newboard[6], newboard[7] = newboard[7], newboard[6], newboard[5], newboard[4], newboard[3], newboard[2], newboard[1], newboard[0]
        return {"result": result, "previous": move[2], "next": move[3], "response": move[4], "board": newboard, "disabled_white_pieces": board.disabled_white_pieces, "disabled_black_pieces": board.disabled_black_pieces}

if __name__ == '__main__':  
    client = OpenAI()

    m = ''
    b = board()
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}
    print(check_valid(client, b, (1, 4), (3, 4), last_move))
    b.print_board()

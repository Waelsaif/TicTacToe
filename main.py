from math import inf as infinity
from random import choice
import time
from tkinter import Tk, Button
from tkinter.font import Font
from copy import deepcopy

HUMAN = -1
AI = +1

board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

class Board:
    
    def wins(state, X):
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [X, X, X] in win_state:
            return True
        else:
            return False

    def evaluateFunction(state):
        if Board.wins(state, AI):
            score = +1
        elif Board.wins(state, HUMAN):
            score = -1
        else:
            score = 0

        return score


    def game_over(state):
        return Board.wins(state, HUMAN) or Board.wins(state, AI)


    def empty_cells(state):
        cellsList = []

        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell == 0:
                    cellsList.append([x, y])

        return cellsList


    def valid_move(x, y):
        if [x, y] in Board.empty_cells(board):
            return True
        else:
            return False


    def set_move(x, y, player):
        if Board.valid_move(x, y):
            board[x][y] = player
            return True
        else:
            return False
        
        
    def minimax(state, depth, player):
        if player == AI:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or Board.game_over(state):
            score = Board.evaluateFunction(state)
            return [-1, -1, score]

        for cell in Board.empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = Board.minimax(state, depth - 1, -player)
            state[x][y] = 0
            score[0], score[1] = x, y

            if player == AI:
                if score[2] > best[2]:
                    best = score  
            else:
                if score[2] < best[2]:
                    best = score  

        return best

    def printBoard(state, AIchoice, HumanChoice):
        chars = {
            -1: HumanChoice,
            +1: AIchoice,
            0: ' '
        }
        str_line = '---------------'

        print('\n' + str_line)
        for row in state:
            for cell in row:
                symbol = chars[cell]
                print(f'| {symbol} |', end='')
            print('\n' + str_line)


    def computer(AIchoice, HumanChoice):
        depth = len(Board.empty_cells(board))
        if depth == 0 or Board.game_over(board):
            return

        print(f'Computer turn [{AIchoice}]')
        Board.printBoard(board, AIchoice, HumanChoice)

        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = Board.minimax(board, depth, AI)
            x, y = move[0], move[1]

        Board.set_move(x, y, AI)
        time.sleep(1)


    def human(AIchoice, HumanChoice):
        depth = len(Board.empty_cells(board))
        if depth == 0 or Board.game_over(board):
            return

        # Dictionary of valid moves
        move = -1
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }

        print(f'Human turn [{HumanChoice}]')
        Board.printBoard(board, AIchoice, HumanChoice)

        while move < 1 or move > 9:
            try:
                move = int(input('Choose from (1..9): '))
                coord = moves[move]
                can_move = Board.set_move(coord[0], coord[1], HUMAN)

                if not can_move:
                    print('Invalid move\n')
                    move = -1
            except (KeyError, ValueError):
                print('CHOOSE AGAIN!\n')

class GUI:
    def main():
        first = ''
        Human = 'X'
        Computer = 'O'

        while first != 'Y' and first != 'N':
            first = input('Want to start first?[y/n]: ').upper()
                    

        while len(Board.empty_cells(board)) > 0 and not Board.game_over(board):
            if first == 'N':
                Board.computer(Computer, Human)
                first = ''

            Board.human(Computer, Human)
            Board.computer(Computer, Human)

            
        if Board.wins(board, HUMAN):
            print(f'Human turn [{Human}]')
            Board.printBoard(board, Computer, Human)
            print('YOU WIN!')
        elif Board.wins(board, AI):
            print(f'Computer turn [{Computer}]')
            Board.printBoard(board, Computer, Human)
            print('YOU LOSE!')
        else:
            Board.printBoard(board, Computer, Human)
            print('DRAW!')
        exit()

GUI.main()
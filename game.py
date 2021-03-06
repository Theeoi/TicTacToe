#!/usr/bin/env python 

import time

from player import Player, HumanPlayer, RandomComputerPlayer, SmartComputerPlayer

class TicTacToe:
    def __init__(self) -> None:
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self) -> None:
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums() -> None:
        for row in [[str(i) for i in range(j*3+1, (j+1)*3+1)] for j in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
            
    def available_moves(self) -> list[int]:
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self) -> bool:
        return ' ' in self.board

    def num_empty_squares(self) -> int:
        return self.board.count(' ')

    def make_move(self, square: int, letter: str) -> bool:
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square: int, letter: str) -> bool: # Checks if there are 3 in a row anywhere.
        # Checking rows
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind + 1)*3]
        if all([spot == letter for spot in row]):
            return True

        # Checking columns
        col_ind = square % 3
        column = [self.board[col_ind + i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Checking diagonals [1, 5, 9] or [3, 5, 7]
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True

            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False

        
def play(game: TicTacToe, x_player: Player, o_player: Player, print_game: bool = True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if letter == 'X':
            square = x_player.get_move(game)
        else:
            square = o_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square + 1}')
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter

            letter = 'O' if letter == 'X' else 'X'

        if isinstance(x_player, HumanPlayer) or isinstance(o_player, HumanPlayer):
            time.sleep(.8)

    if print_game:
        print('It\'s a tie!')


if __name__ == '__main__':
    x_wins, o_wins, ties = [0, 0, 0]

    num_iter = 10
    for _ in range(num_iter):
        x_player = RandomComputerPlayer('X')
        o_player = SmartComputerPlayer('O')
        t = TicTacToe()
        result = play(t, x_player, o_player, print_game=True)

        if result == 'X':
            x_wins += 1
        elif result == 'O':
            o_wins += 1
        else:
            ties += 1

    print(f'From {num_iter} games played we have {x_wins} X-wins, {o_wins} O-wins and {ties} ties.')


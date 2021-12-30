
from __future__ import annotations
import random
import math

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import TicTacToe

class Player:
    def __init__(self, letter: str) -> None:
        self.letter = letter # letter is X or O


class RandomComputerPlayer(Player):
    def __init__(self, letter: str) -> None:
        super().__init__(letter)

    def get_move(self, game: TicTacToe) -> int:
        square = random.choice(game.available_moves()) # Get a random available spot for our next move
        return square


class HumanPlayer(Player):
    def __init__(self, letter: str) -> None:
        super().__init__(letter)

    def get_move(self, game: TicTacToe) -> int:
        valid_square = False
        val = -1
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (1-9):')
            try:
                val = int(square)
                if val not in [i+1 for i in game.available_moves()]:
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        
        return val - 1


class SmartComputerPlayer(Player):
    def __init__(self, letter: str) -> None:
        super().__init__(letter)

    def get_move(self, game: TicTacToe) -> int:
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) # Get a random available spot for our next move
        else:
            square = self.minimax(game, self.letter)['position']
        
        return square

    def minimax(self, state: TicTacToe, player: str) -> dict: 
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player
                            else -1 * (state.num_empty_squares() + 1)
                    }
        elif not state.empty_squares():
            return {'position': None,
                    'score': 0
                    }

        if player == max_player:
            best = {'position': None,
                    'score': -math.inf # Score should be maximized
                    }
        else:
            best = {'position': None,
                    'score': math.inf # Score should be minimized
                    }

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)

            # Simulate the game after above move and switch player
            sim_score = self.minimax(state, other_player) 

            state.board[possible_move] = ' ' # Undo move
            state.current_winner = None
            sim_score['position'] = possible_move # Update position

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best 




import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Represents the Tic-Tac-Toe board

    def print_board(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        self.board[square] = letter

    def make_random_move(self, letter):
        square = random.choice(self.available_moves())
        self.make_move(square, letter)

    def print_board_nums(self):
        board_nums = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in board_nums:
            print('| ' + ' | '.join(row) + ' |')

    def play_game(self, x_player, o_player):
        letter = 'X'  # Starting player
        while self.empty_squares():
            if letter == 'O':
                square = o_player.choose_square(self)
                print("\nComputer's Move:")
            else:
                print("\nYour Move:")
                square = x_player.choose_square(self)

            if self.board[square] != ' ':
                continue

            self.make_move(square, letter)
            #print("\nCurrent Board:")
            self.print_board()

            if self.winner(letter):
                print(f"{letter} wins!")
                return letter  # Ends the game

            letter = 'O' if letter == 'X' else 'X'  # Switch player

        print("It's a tie!")

    def winner(self, letter):
        # Check rows, columns, and diagonals for a winner
        return any(
            all(self.board[i] == letter for i in row)
            for row in [
                [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
                [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
                [0, 4, 8], [2, 4, 6]  # Diagonals
            ]
        )

#class RandomPlayer:
    #def choose_square(self, game):
        #return random.choice(game.available_moves())

class MinMaxPlayer:
    def choose_square(self, game):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for move in game.available_moves():
            game.make_move(move, 'O')  # Assume the move for the AI player
            score = self.minimax(game, 0, False, alpha, beta)
            game.make_move(move, ' ')  # Undo the move

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        return best_move

    def minimax(self, game, depth, is_maximizing, alpha, beta):
        scores = {'X': -1, 'O': 1, 'tie': 0}

        if game.winner('O'):
            return scores['O']
        elif game.winner('X'):
            return scores['X']
        elif not game.empty_squares():
            return scores['tie']

        if is_maximizing:
            best_score = float('-inf')
            for move in game.available_moves():
                game.make_move(move, 'O')
                score = self.minimax(game, depth + 1, False, alpha, beta)
                game.make_move(move, ' ')
                best_score = max(score, best_score)

                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break

            return best_score
        else:
            best_score = float('inf')
            for move in game.available_moves():
                game.make_move(move, 'X')
                score = self.minimax(game, depth + 1, True, alpha, beta)
                game.make_move(move, ' ')
                best_score = min(score, best_score)

                beta = min(beta, best_score)
                if alpha >= beta:
                    break

            return best_score



class HumanPlayer:
    def choose_square(self, game):
        square = None
        while square not in game.available_moves():
            try:
                square = int(input("Choose a square (0-8): "))
            except ValueError:
                print("Invalid input. Please enter a number.")

        return square

if __name__ == "__main__":
    x_player = HumanPlayer()  # You are the X player
    o_player = MinMaxPlayer()  # The computer is the O player using MinMax

    game = TicTacToe()
    game.play_game(x_player, o_player)

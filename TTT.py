# min max pruning

import tkinter as tk

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def is_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def min_max(board, depth, is_max):
    scores = {
        'X': 1,
        'O': -1,
        'draw': 0
    }

    if is_winner(board, 'X'):
        return -1
    if is_winner(board, 'O'):
        return 1
    if is_draw(board):
        return 0

    if is_max:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = min_max(board, depth + 1, False)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = min_max(board, depth + 1, True)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval

def best_move(board):
    best_eval = float('-inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                eval = min_max(board, 0, False)
                board[i][j] = ' '
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)

    return best_move


def update_board(row, col):
    global player
    if board[row][col] == ' ':
        board[row][col] = player
        buttons[row][col].config(text=player)
        if is_winner(board, player):
            result_label.config(text=f'Player {player} wins!')
        elif is_draw(board):
            result_label.config(text='It\'s a draw!')
        else:
            player = 'O' if player == 'X' else 'X'
            if player == 'O':
                row, col = best_move(board)
                update_board(row, col)

def create_buttons():
    for i in range(3):
        row_buttons = []
        for j in range(3):
            btn = tk.Button(root, text='', font=('normal', 40), width=4, height=2, command=lambda i=i, j=j: update_board(i, j))
            btn.grid(row=i, column=j, padx=5, pady=5)
            row_buttons.append(btn)
        buttons.append(row_buttons)

def main():
    global root, result_label, buttons, board, player

    root = tk.Tk()
    root.title("Tic-Tac-Toe")
    result_label = tk.Label(root, text='', font=('normal', 14))
    result_label.grid(row=3, column=0, columnspan=3, pady=10)
    buttons = []

    create_buttons()

    player = 'X'
    board = [[' ' for _ in range(3)] for _ in range(3)]

    root.mainloop()

if __name__ == "__main__":
    main()

#tic tac toe
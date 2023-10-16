import streamlit as st
import numpy as np
import asyncio #asyncio is a library to write concurrent code using the async/await syntax.
### new code #####
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
    return all(cell != "." for row in board for cell in row)

###Old repurpose###
def checkWin(board):
    # transposition to check rows, then columns
    for newBoard in [board, np.transpose(board)]:
        result = is_winner(newBoard,"X")
        if result:
         return result
        result = is_winner(newBoard,"O")
        if result:
          return result
        

### new code #####

@st.cache_resource()# Decorator to cache functions that return global
def board():
    return np.full((3, 3), ".", dtype=str)

@st.cache_resource()
def select_next_player():
    return ["X"]

async def watch():
    while True:
        game_board = board()
        if "online_board" not in st.session_state:
            local_game_board = np.copy(game_board)
        else:
            local_game_board = st.session_state.online_board
        if not np.array_equal(game_board, local_game_board):
            st.experimental_rerun()
        _ = await asyncio.sleep(1)


def plot_game_board(game_board, i_am):
    # Show one button for each field.
    st.session_state.online_board = np.copy(game_board)
    for i, row in enumerate(game_board):
        cols = st.columns([0.1, 0.1, 0.1, 0.1, 0.1, 0.5])
        for j, field in enumerate(row):
            cols[j].button(
                field,
                key=f"ttt_online_{i}-{j}",
                on_click=handle_click,
                args=(i, j, i_am),
            )
    btn_reset = st.button("Reset")
    if btn_reset:
            reset_game()
    winner = checkWin(game_board)
    if winner != False:
        st.session_state.winner = winner



def reset_game():
    st.session_state.winner = False
    # clear cache
    st.cache_data.clear()
    st.cache_resource.clear()

 

def handle_click(i, j, i_am):
    game_board = board()
    next_player = select_next_player()

    if not st.session_state.winner or st.session_state.winner == ".":
        if i_am == next_player[0]:
            if game_board[i, j] == ".":
                game_board[i, j] = next_player[0]
                next_player[0] = ("O" if next_player[0] == "X" else "X")
            else:
                st.warning("Select an empty box")
        else:
            st.warning("It is not your turn")


def tictactoe_online():
   
    st.write("")
    st.write("""
        In this game, two players can play together from different devices.
        It is possible for the other users to join and watch the players' game.
    """)
    i_am = st.radio("Who are you?", options=["X", "O"])

    # Initialize state.
    game_board = board()
    next_player = select_next_player()

    if "winner" not in st.session_state:
        st.session_state.winner = None

    st.info(f"**{next_player[0]}** turn")

    plot_game_board(game_board, i_am)


    asyncio.run(watch())


if __name__ == '__main__':
    tictactoe_online()

import streamlit as st
from firebase_configttt import init_firebase
import firebase_admin
from firebase_admin import db
import time

# Initialize Firebase
if not firebase_admin._apps:
    init_firebase()

st.title("🎮 Multiplayer Tic Tac Toe")

# Inputs
room_code = st.text_input("Enter Room Code")
player_name = st.text_input("Enter Your Name")
join = st.button("Join Game")

# Proceed if both inputs are filled
if room_code and player_name:
    if join:
        room_ref = db.reference(f"/rooms/{room_code}")
        try:
            room = room_ref.get()
        except Exception as e:
            st.error(f"Error accessing Firebase: {e}")
            st.stop()

        if not room:
            # Create new room
            room_ref.set({
                "board": [""] * 9,
                "turn": "X",
                "player_X": player_name,
                "player_O": "",
                "status": "waiting",
                "winner": None
            })
            st.success("Room created. Waiting for another player...")
            st.stop()
        else:
            if room["player_O"] == "":
                room_ref.update({"player_O": player_name, "status": "playing"})
                st.success("You joined as Player O.")
            else:
                st.error("Room is full.")
                st.stop()

    # Always refresh the room state
    room_ref = db.reference(f"/rooms/{room_code}")
    room = room_ref.get()

    # Display game info
    st.write(f"Player X: {room['player_X']}")
    st.write(f"Player O: {room['player_O']}")
    st.write(f"Status: {room['status']}")
    st.write(f"Current turn: {room['turn']}")

    if room["status"] == "waiting":
        st.warning("Waiting for second player to join...")
        st.stop()

    # Game Board
    board = room["board"]
    cols = st.columns(3)

    for i in range(9):
        with cols[i % 3]:
            if st.button(board[i] or " ", key=i):
                if board[i] == "" and room["status"] == "playing":
                    is_x = player_name == room["player_X"]
                    is_o = player_name == room["player_O"]
                    if (room["turn"] == "X" and is_x) or (room["turn"] == "O" and is_o):
                        board[i] = room["turn"]
                        room["turn"] = "O" if room["turn"] == "X" else "X"

                        # Win check
                        win = None
                        combos = [
                            [0, 1, 2], [3, 4, 5], [6, 7, 8],
                            [0, 3, 6], [1, 4, 7], [2, 5, 8],
                            [0, 4, 8], [2, 4, 6]
                        ]
                        for c in combos:
                            a, b, c_ = c
                            if board[a] == board[b] == board[c_] and board[a] != "":
                                win = board[a]
                                break

                        if win:
                            room["winner"] = win
                            room["status"] = "finished"
                        elif all(cell != "" for cell in board):
                            room["winner"] = "Draw"
                            room["status"] = "finished"

                        room["board"] = board
                        room_ref.set(room)
                        st.experimental_rerun()

    # Result
    if room["status"] == "finished":
        if room["winner"] == "Draw":
            st.success("😐 Match Drawn!")
        else:
            st.success(f"🏆 {room['winner']} wins the game!")

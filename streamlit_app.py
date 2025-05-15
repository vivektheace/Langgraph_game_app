import time
import logging
import streamlit as st
from graph.langgraph_config import build_langgraph
from db.history import init_db, get_history, log_game

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize SQLite DB
init_db()

# Streamlit App Title
st.title("LangGraph Game App")

# Username input
username = st.text_input("Enter your username", value="guest")

if username:
    graph_app = build_langgraph(username)
    menu_choice = st.radio("Select an option:", ["Main Menu", "Number Game", "Word Game", "View History"])

    # === Number Game ===
    if menu_choice == "Number Game":
        st.info("Think of a number between 1 and 50.")
        
        # Initialize state
        if "low" not in st.session_state:
            st.session_state.low = 1
            st.session_state.high = 50
            st.session_state.attempts = 0
            st.session_state.start_time = time.time()
            st.session_state.finished = False

        if not st.session_state.finished and st.session_state.low <= st.session_state.high:
            mid = (st.session_state.low + st.session_state.high) // 2
            st.write(f"Is your number greater than {mid}?")
            col1, col2 = st.columns(2)
            if col1.button("Yes"):
                st.session_state.low = mid + 1
                st.session_state.attempts += 1
            if col2.button("No"):
                st.session_state.high = mid - 1
                st.session_state.attempts += 1
        else:
            st.session_state.finished = True
            duration = time.time() - st.session_state.start_time
            st.success(f"Your number is {st.session_state.low}")
            st.write(f"Guessed in {st.session_state.attempts} attempts.")
            st.write(f"Took {duration:.2f} seconds.")
            if st.button("Finish & Return to Menu"):
                graph_app.invoke({"input": "1", "username": username})
                log_game(username, "number", True, duration, st.session_state.attempts)
                for key in ["low", "high", "attempts", "start_time", "finished"]:
                    del st.session_state[key]

    # === Word Game ===
    elif menu_choice == "Word Game":
        st.info("Pick a word from this list (do not type it):")
        word_list = ["apple", "chair", "elephant", "guitar", "rocket", "pencil", "pizza", "tiger"]
        st.write(", ".join(word_list))

        if "word_clues" not in st.session_state:
            st.session_state.word_clues = [""] * 5
            st.session_state.word_start_time = time.time()
            st.session_state.word_guess_made = False
            st.session_state.word_success = False

        for i in range(5):
            st.session_state.word_clues[i] = st.text_input(
                f"Clue {i+1} (yes/no/maybe):", 
                value=st.session_state.word_clues[i], 
                key=f"clue_{i}"
            )

        if not st.session_state.word_guess_made and st.button("Guess"):
            guess = "apple"
            user_response = st.radio(f"Is your word '{guess}'?", ["Yes", "No"], key="final_guess")
            if user_response:
                st.session_state.word_guess_made = True
                st.session_state.word_success = user_response == "Yes"
                duration = time.time() - st.session_state.word_start_time
                attempts = 5
                graph_app.invoke({"input": "2", "username": username})
                log_game(username, "word", st.session_state.word_success, duration, attempts)

        if st.session_state.word_guess_made:
            if st.session_state.word_success:
                st.success("The word was guessed correctly.")
            else:
                st.error("The guess was incorrect.")
            if st.button("Finish & Return to Menu", key="word_done"):
                for key in ["word_clues", "word_start_time", "word_guess_made", "word_success"]:
                    del st.session_state[key]

    # === Game History ===
    elif menu_choice == "View History":
        logs = get_history(username)
        if logs:
            st.subheader("Game History")
            for row in logs:
                st.write(
                    f"[{row[6]}] {row[2].title()} - {'Success' if row[3] else 'Fail'} - "
                    f"{row[4]:.1f}s, {row[5]} attempts"
                )
        else:
            st.info("No history found.")

    else:
        st.info("Select a game to start.")

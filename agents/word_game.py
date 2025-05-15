import logging
import time
from db.history import log_game

logger = logging.getLogger(__name__)

WORD_LIST = [
    "apple", "chair", "elephant", "guitar",
    "rocket", "pencil", "pizza", "tiger"
]

def word_game_agent(state: dict) -> str:
    """
    Runs the word guessing game where the agent asks 5 descriptive questions
    and tries to guess the user's selected word from a fixed list.

    Args:
        state (dict): Contains the session object and username.

    Returns:
        str: The next node to transition to in the LangGraph ("selector" or "word_game").
    """
    session = state["session"]
    username = state.get("username", "guest")

    print("\nPick a word from this list (but don't tell me):")
    print(", ".join(WORD_LIST))
    input("Press Enter when ready...")

    print("\nI'll ask you 5 yes/no/maybe questions.")
    logger.info(f"User '{username}' started Word Game.")
    start_time = time.time()
    attempts = 5

    for i in range(5):
        clue = input(f"Question {i+1}: (Type yes/no/maybe): ").strip()
        logger.debug(f"Clue {i+1} from user '{username}': {clue}")

    guess = "apple"
    response = input(f"\nIs your word '{guess}'? (yes/no): ").strip().lower()
    success = response == "yes"
    duration = time.time() - start_time

    if success:
        print("I guessed it correctly.")
        logger.info(f"Word Game success for user '{username}' in {duration:.2f} seconds.")
    else:
        print("I didn't guess it right.")
        logger.info(f"Word Game failed for user '{username}' in {duration:.2f} seconds.")
        retry = input("Do you want to retry the game? (yes/no): ").strip().lower()
        if retry == "yes":
            return "word_game"

    session.increment_word_game()

    log_game(
        username=username,
        game_type="word",
        success=success,
        duration=duration,
        num_attempts=attempts
    )

    return "selector"

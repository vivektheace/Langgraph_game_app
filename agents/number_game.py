import logging
import time
from db.history import log_game

logger = logging.getLogger(__name__)

def number_game_agent(state: dict) -> str:
    """
    Executes the number guessing game using binary search logic.
    Tracks the number of attempts, duration, and logs the result.

    Args:
        state (dict): Includes session object and username.

    Returns:
        str: The next node to transition to in the LangGraph ("selector").
    """
    session = state["session"]
    username = state.get("username", "guest")

    print("\nThink of a number between 1 and 50. I will try to guess it.")
    logger.info(f"User '{username}' started Number Game.")

    low, high = 1, 50
    attempts = 0
    start_time = time.time()

    while low <= high:
        mid = (low + high) // 2
        response = input(f"Is your number greater than {mid}? (yes/no): ").strip().lower()
        attempts += 1
        logger.debug(f"Attempt {attempts}: Asked about {mid}, response: {response}")

        if response == "yes":
            low = mid + 1
        elif response == "no":
            high = mid - 1
        else:
            print("Please answer with 'yes' or 'no'.")
            logger.warning(f"Invalid input '{response}' received. Expecting 'yes' or 'no'.")

    duration = time.time() - start_time
    print(f"\nYour number is {low}!\n")
    logger.info(f"Number Game completed by '{username}' in {attempts} attempts and {duration:.2f} seconds.")

    session.increment_number_game()

    log_game(
        username=username,
        game_type="number",
        success=True,
        duration=duration,
        num_attempts=attempts
    )

    return "selector"

import logging

logger = logging.getLogger(__name__)

def game_selector_agent(state: dict) -> str:
    """
    Routes the user input to the corresponding game node.

    Args:
        state (dict): Contains the input string and session context.

    Returns:
        str: The name of the next node in the LangGraph.
    """
    user_input = state.get("input", "").strip()

    logger.info(f"User selected option: '{user_input}'")

    if user_input == "1":
        return "number_game"
    elif user_input == "2":
        return "word_game"
    elif user_input.lower() == "exit":
        return "end"
    else:
        logger.warning("Invalid input received. Returning to selector.")
        print("Invalid input. Please try again.")
        return "selector"

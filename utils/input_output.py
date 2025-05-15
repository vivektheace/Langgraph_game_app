import logging

logger = logging.getLogger(__name__)

def main_menu() -> str:
    """
    Displays the main menu options and captures the user's choice.

    Returns:
        str: The selected menu option as a stripped string.
    """
    print("\nChoose a game:")
    print("1. Number Game")
    print("2. Word Game")
    print("3. View History")
    print("(Leave blank to exit)")

    choice = input(">> ").strip()
    logger.info(f"Main menu option selected: '{choice}'")
    return choice

import logging

logger = logging.getLogger(__name__)

class SessionState:
    """
    Tracks session-level statistics for a single user across multiple games.
    Maintains counters for word and number games played.
    """

    def __init__(self):
        self.word_game_count = 0
        self.number_game_count = 0
        logger.info("Initialized new session state.")

    def increment_word_game(self):
        """
        Increments the counter for word games played.
        """
        self.word_game_count += 1
        logger.debug(f"Word game count incremented to {self.word_game_count}.")

    def increment_number_game(self):
        """
        Increments the counter for number games played.
        """
        self.number_game_count += 1
        logger.debug(f"Number game count incremented to {self.number_game_count}.")

    def summary(self) -> str:
        """
        Returns a formatted summary string of the games played in this session.

        Returns:
            str: Summary of game counts.
        """
        summary_text = (
            f"\nYou played {self.word_game_count} word game(s) "
            f"and {self.number_game_count} number game(s).\n"
        )
        logger.info("Session summary generated.")
        return summary_text

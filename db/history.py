import sqlite3
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

# Define path to the SQLite database
DB_PATH = os.path.join(os.path.dirname(__file__), "history.db")

def init_db():
    """
    Initializes the SQLite database by creating the 'game_logs' table if it does not exist.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS game_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    game_type TEXT,
                    success INTEGER,
                    duration REAL,
                    num_attempts INTEGER,
                    timestamp TEXT
                )
            ''')
            conn.commit()
            logger.info("Database initialized and table 'game_logs' ensured.")
    except sqlite3.Error as e:
        logger.error(f"Database initialization failed: {e}")
        raise

def log_game(username: str, game_type: str, success: bool, duration: float, num_attempts: int):
    """
    Inserts a log entry for a completed game into the 'game_logs' table.

    Args:
        username (str): The name of the user.
        game_type (str): Type of game played ("number" or "word").
        success (bool): Whether the game was completed successfully.
        duration (float): Duration of the game in seconds.
        num_attempts (int): Number of attempts made in the game.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO game_logs (username, game_type, success, duration, num_attempts, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, game_type, int(success), duration, num_attempts, datetime.now().isoformat()))
            conn.commit()
            logger.info(f"Game log inserted for user '{username}' - {game_type}, success: {success}, attempts: {num_attempts}, duration: {duration:.2f}s")
    except sqlite3.Error as e:
        logger.error(f"Failed to log game for user '{username}': {e}")
        raise

def get_history(username: str = None):
    """
    Retrieves the game history from the 'game_logs' table.

    Args:
        username (str, optional): Filter history by this username. If None, returns all history.

    Returns:
        list: A list of tuples representing the game history records.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if username:
                logger.debug(f"Fetching history for user '{username}'.")
                cursor.execute(
                    "SELECT * FROM game_logs WHERE username = ? ORDER BY timestamp DESC", 
                    (username,)
                )
            else:
                logger.debug("Fetching complete game history.")
                cursor.execute("SELECT * FROM game_logs ORDER BY timestamp DESC")
            return cursor.fetchall()
    except sqlite3.Error as e:
        logger.error(f"Failed to fetch game history: {e}")
        raise

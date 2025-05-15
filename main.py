import logging
from utils.input_output import main_menu
from graph.langgraph_config import build_langgraph
from db.history import init_db, get_history

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    """
    Entry point for the CLI-based LangGraph game application.
    Initializes the database, prompts for a username,
    and handles routing to game logic or history view.
    """
    init_db()
    username = input("Enter your username: ").strip() or "guest"
    logger.info(f"User '{username}' started a new session.")

    graph_app = build_langgraph(username)

    while True:
        user_input = main_menu()

        if user_input == "":
            logger.info(f"User '{username}' exited the session.")
            graph_app.invoke({"input": "exit", "username": username})
            break

        elif user_input == "3":
            logs = get_history(username)
            print("\nYour Game History:")
            if logs:
                for row in logs:
                    print(f"[{row[6]}] {row[2].title()} - {'Success' if row[3] else 'Fail'} - {row[4]:.1f}s, {row[5]} attempts")
                logger.info(f"Displayed game history for user '{username}'.")
            else:
                print("No game history found.")
                logger.info(f"No history found for user '{username}'.")

        else:
            logger.info(f"Routing user '{username}' input '{user_input}' to graph.")
            graph_app.invoke({"input": user_input, "username": username})

if __name__ == "__main__":
    main()

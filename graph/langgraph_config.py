import logging
from langgraph.graph import StateGraph
from pydantic import BaseModel
from agents.game_selector import game_selector_agent
from agents.number_game import number_game_agent
from agents.word_game import word_game_agent
from state.session import SessionState

logger = logging.getLogger(__name__)

class GameState(BaseModel):
    """
    Defines the schema for state passed through the LangGraph nodes.
    """
    input: str
    username: str

def build_langgraph(username: str):
    """
    Constructs and compiles a LangGraph representing the game state machine.

    Nodes:
        - selector: Routes to number_game, word_game, or end
        - number_game: Handles binary search guessing game
        - word_game: Handles clue-based word guessing game
        - end: Prints session summary

    Returns:
        Callable graph object to invoke with GameState input.
    """
    logger.info(f"Building LangGraph for user '{username}'")

    session = SessionState()

    def wrap_agent(func):
        """
        Injects session and username into all agent functions for consistent context.
        """
        return lambda state: func({
            "input": state.input,
            "session": session,
            "username": state.username
        })

    # Initialize graph with state schema
    builder = StateGraph(state_schema=GameState)

    # Selector is a router node that conditionally forwards
    builder.add_conditional_edges(
        "selector",
        wrap_agent(game_selector_agent),
        {
            "number_game": "number_game",
            "word_game": "word_game",
            "end": "end"
        }
    )

    # Register agent nodes
    builder.add_node("number_game", wrap_agent(number_game_agent))
    builder.add_node("word_game", wrap_agent(word_game_agent))
    builder.add_node("end", lambda _: print(session.summary()))

    # Ensure selector can be returned to (target of transitions)
    builder.add_node("selector", lambda state: None)

    # Define flow: return to selector after game completion
    builder.set_entry_point("selector")
    builder.add_edge("number_game", "selector")
    builder.add_edge("word_game", "selector")

    logger.info("LangGraph compiled successfully.")
    return builder.compile()


````markdown
# LangGraph Multi-Agent Game App

This project is a modular, multi-agent, multi-turn game application built using [LangGraph](https://github.com/langchain-ai/langgraph). It supports both CLI and Streamlit-based UI, uses SQLite for persistent game history, and demonstrates best practices in agent orchestration, session state management, and metrics logging.

---

## Features

- Binary search-based **Number Game**
- Clue-driven **Word Guessing Game**
- Modular agent logic using **LangGraph**
- Session-aware gameplay with counters
- Persistent game history using **SQLite**
- Dual interface: **Command-Line Interface** and **Streamlit UI**
- Fully containerized with **Docker**

---

## Project Structure

```text
game_app/
├── agents/             # Modular agents
├── db/                 # SQLite logging logic
├── graph/              # LangGraph configuration
├── state/              # Session state tracker
├── utils/              # Input/output helpers
├── main.py             # CLI entry point
├── streamlit_app.py    # Streamlit UI app
├── requirements.txt
├── Dockerfile
├── entrypoint.sh
└── .dockerignore
````

---

## Getting Started (Locally)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run CLI Mode

```bash
python main.py
```

### 3. Run Streamlit UI

```bash
streamlit run streamlit_app.py
```

---

## Docker Support

### 1. Build the Docker image

```bash
docker build -t game-app .
```

### 2. Run in CLI Mode

```bash
docker run --rm -it game-app cli
```

### 3. Run in Streamlit UI Mode

```bash
docker run --rm -p 8501:8501 game-app ui
```

Then open: [http://localhost:8501](http://localhost:8501)

---

## Game Metrics Tracked

Each game session is logged in `db/history.db` with:

* Username
* Game type (`number` or `word`)
* Success status
* Duration (in seconds)
* Number of attempts
* Timestamp

---

## Built With

* [LangGraph](https://github.com/langchain-ai/langgraph)
* [Streamlit](https://streamlit.io/)
* Python 3.10+

---

## License

This project is for evaluation and demonstration purposes only.

```

---

```

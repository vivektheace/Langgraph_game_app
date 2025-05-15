#!/bin/bash

MODE=$1

if [ "$MODE" == "ui" ]; then
  echo "Launching Streamlit UI..."
  streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
else
  echo "Launching CLI mode..."
  python main.py
fi

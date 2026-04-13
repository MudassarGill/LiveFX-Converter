# LiveFX-Converter

A real-time foreign exchange (FX) converter that uses live APIs to convert currencies instantly with high accuracy. The project features an AI agent powered by `Langchain`, dynamically choosing between `Groq` and `Hugging Face` for inference. It has a beautiful **Streamlit UI** connected to a robust **FastAPI backend**.

## Architecture Overview

1. **`core/agent.py`**: The brain of the app. It connects to Groq (or falls back to HuggingFace Llama if Groq is unavailable) and uses tools to fetch real-time exchange rates.
2. **`api.py`**: The FastAPI backend. It provides a REST endpoint at `/chat` making the AI agent available to any client.
3. **`app.py`**: The Streamlit user interface. It communicates via HTTP requests with the FastAPI backend.
4. **`main.py`**: The unified launcher script. One command to start both servers.

## Prerequisites

1. Create a `.env` file in the root directory (already done if you cloned this locally).
2. Ensure you have the required API keys inside. Your `.env` should look like this:
   ```env
   GROQ_API_KEY=gsk_...
   HUGGINGFACE_API_KEY=hf_...
   EXCHANGE_RATE_API_KEY=your_exchange_api_key_here
   ```

## Installation

Ensure all required Python dependencies are installed. You can install them by running:
```bash
pip install fastapi uvicorn streamlit langchain langchain-groq langchain-huggingface python-dotenv requests
```

## Running the Application

To make it incredibly easy, you only need to run a **single command** to start both the Frontend UI and Backend API!

```bash
python main.py
```

This will:
1. Start the FastAPI backend on `http://127.0.0.1:8000`.
2. Start the Streamlit frontend on `http://127.0.0.1:8501`.
3. Open your browser to the Streamlit UI automatically.

### Alternative (Run Individually)

If you'd like to test or debug them separately, use two different terminal windows:

Terminal 1 (Backend):
```bash
uvicorn api:app --reload
```

Terminal 2 (Frontend):
```bash
streamlit run app.py
```

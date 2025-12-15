# Assistant Revamped

A Python-based assistant application using OpenRouter for AI completions.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd assistant-revamped
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/macOS
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration:**
    Copy the example environment file and configure your API keys.
    ```bash
    cp .env.example .env
    ```
    Open `.env` and fill in your `OPENROUTER_API_KEY` and `OPENROUTER_MODEL`.

## Usage

Run the application using Python:

```bash
python src/main.py
```

## Features

- GUI interface (Tkinter based on file structure inference).
- Integration with OpenRouter API.
- Chat history management.

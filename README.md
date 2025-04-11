# Overview & Features

This is an AI-powered chatbot app where the chatbot can initate conversations instead of waiting for you to prompt it

## Tech_overview for devs

For developers, see [Tech_overview](README_tech_overview.md) to learn more about the techical detail of the project (which files are for what, tech stack etc.)

## Prerequisites

1. **Python 3.11+**: If Python is not installed, you need to install it. You can download the appropriate version from the official Python website: [Python Downloads](https://www.python.org/downloads/).
2. **Node.js**: If Nodejs is not installed, you need to install it. Install Node.js from the official website: [Node.js Downloads](https://nodejs.org/). Node.js comes with npm (Node Package Manager), which is used for managing frontend dependencies.

## Backend Setup (Python)

### 1. Navigate to the backend directory
Open your terminal and run the following command:

```bash
cd ./backend
```

### 2. Set up a virtual environment
Run the following command in the terminal to create a virtual environment named `.venv`:

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

- **On Windows** (Command Prompt or PowerShell):

  ```plaintext
  .venv\Scripts\activate
  ```

- **On Linux or macOS**:

  ```bash
  source .venv/bin/activate
  ```

### 4. Install Python packages

Ensure you have a `requirements.txt` file in your backend directory. Then run:

```bash
pip install -r requirements.txt
```

## Frontend Setup

### 1. Navigate to the frontend directory

```bash
cd ../frontend
```

### 2. Install the necessary npm modules

```bash
npm install
```

## Environment Variables Setup

1. Locate the `.env.example` file in your project (in the root directory).
2. Rename the file to `.env`:

   ```bash
   mv .env.example .env
   ```

3. Go to [OpenRouter](https://openrouter.ai/) and create an account.
4. Paste your API key into the `.env` file.
5. (Optional) Follow any additional steps mentioned in the original `.env.example` file.

## How to Run

To run the app, start two servers (backend and frontend):

### 1. Start the Backend Server

In the root directory, run (or without \backend in the backend directory):

```bash
fastapi dev backend\main.py
```

Here, `main` is the Python file name (usually `main.py`). 

### 2. Start the Frontend Server

Open a new terminal, navigate to the frontend directory, and run:

```bash
npm run dev
```

Click the generated URL in the terminal to view the frontend in your browser.

## How to Stop

### Backend Server
To stop the backend server, kill the terminal.

### Frontend Server
To stop the frontend server, press `Ctrl + C` in the terminal where it is running.

## How to Run Tests on the backend
Navigate to the root directory and run:

```bash
backend.test.name_of_the_test_file_without_dot_py
```

for example:

```bash
backend.test.test_graph
```

## Future Improvements

1) UI Features
    - Add "blue ticks" to represent read messages.
    - Display an icon on top to indicate websocket connection status (e.g., bot is online).
    - Add support for dark mode in the settings.
    - Implement a settings tool to toggle "active" conversation mode.
    - Support custom background images/icons.

2) Chat History
    - Trim chat history when it becomes too long.

3) Better Decision-Making from the `should_I_talk` Bot
    - Feed only the few most recent chat messages to the `should_I_talk` function instead of the entire message.    
    -  Use better prompts for improved behavior.
    - Allow the bot's personality to influence its decisions appropriately.

4) Personality Customization
    - Allow UI-based bot personality customization.
    - Forward updates to the LangGraph state (requires UI update).

5) Checkpointing, Threads, Multi-Chat Support, and Database Management
    - Upgrade from in-memory checkpointing to database checkpointing.
    - Support multiple chats, each running with a different thread ID (requires UI update).

6) Train/Finetune Custom LLM Models
    - Train a specialized model for roleplay (chatbot).
    - Train a specialized model for assessing conversational cues to decide whether the bot should talk.


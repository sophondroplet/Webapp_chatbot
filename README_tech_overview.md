# Technical Overview of the GitHub Project

## Project Structure and Tech Stack
This is a web application consisting of a frontend built with TypeScript, React, and Vite, and a backend powered by Python and FastAPI. The primary communication mechanism between the frontend and backend is through WebSockets, with HTTP requests used for initialization.

### Frontend
The frontend is a TypeScript React application created with Vite. Most of the files in the frontend directory are configuration files. The main files and directories are as follows:

#### Key Files and Directories
- **`App.tsx`**: This file manages the overall application logic and communication. It initializes the chat session by making an HTTP POST request to the backend to create a new thread. It also sets up the WebSocket connection to the backend and handles incoming WebSocket messages to update the chat message history.
- **`components` Directory**: Contains files that hold the logic for specific components. For example, `ChatWindow.tsx` is responsible for rendering the chat window, handling user input, and sending messages to the backend via WebSocket.

#### Configuration Files
- **`package-lock.json`**: Records the exact versions of all the npm packages installed in the project, ensuring reproducible builds.
- **`.gitignore`**: Specifies files and directories that should be ignored by Git, such as `node_modules`, build artifacts, and log files.
- **`vite.config.ts`**: Configures the Vite build tool, including plugins like `@vitejs/plugin-react` for React support and `@tailwindcss/vite` for Tailwind CSS integration.

#### Recommended Reading
If you are new to React, it is recommended to read the [React documentation](https://reactjs.org/docs/getting-started.html).

### Backend
The backend is a Python application using FastAPI. It leverages OpenRouter to access remotely hosted LLMs, LangGraph to handle the agent workflow, and Pydantic for data validation.

#### Key Files and Their Functions
- **`main.py`**: Houses the FastAPI API endpoints. It defines the WebSocket endpoint `/chat/ws` which accepts WebSocket connections, initializes the chat session, and streams messages to the frontend. It also starts a background process (`timer.monitor_threads`) to monitor user idle time.
- **`graph.py`**: Contains the agentic LLM workflow. The `should_talk` function determines whether the LLM should respond based on the conversation state, such as whether the user has sent a message or left the bot's message on read.
- **`timer.py`**: Implements a background process (async coroutine) that continuously monitors the conversation. It checks for user idle time and, if the threshold is exceeded, prompts the LLM to initiate a conversation with the user.
- **`agents.py`**: Defines all the Agent objects. These objects are LLM endpoints configured with the model type, system prompts, etc.

#### Testing File
- **`tests/test.py`**: Contains test code to verify the functionality of the backend. It tests the streaming of messages from the LLM and the handling of user input.

#### Recommended Reading
- [FastAPI documentation](https://fastapi.tiangolo.com/): For understanding how to work with FastAPI endpoints and WebSockets.
- [OpenRouter documentation](https://openrouter.ai/docs): To learn how to access and make requests to remotely hosted LLMs.
- [LangGraph documentation](Link-to-LangGraph-docs): For details on handling the agent workflow.
- [Pydantic documentation](https://pydantic-docs.helpmanual.io/): To understand data validation in Python.

## Communication Flow
1. **Initialization**: The frontend (`App.tsx`) makes an HTTP POST request to the backend (`main.py`) to create a new thread. The backend responds with the thread ID and initial messages.
2. **WebSocket Connection**: The frontend establishes a WebSocket connection to the backend. It sends the thread ID to the backend upon connection.
3. **Message Exchange**:
    - **User to Backend**: When the user sends a message in the chat window (`ChatWindow.tsx`), the frontend sends the message to the backend via WebSocket.
    - **Backend to Frontend**: The backend processes the user message using LangGraph and streams the LLM's response to the frontend in chunks via WebSocket. The frontend updates the chat message history accordingly.
4. **Idle Monitoring**: The `timer.py` in the backend continuously monitors the conversation for user idle time. If the user is idle for a certain period, it prompts the LLM to initiate a conversation and sends the response to the frontend via WebSocket.
# Overview & Features

This is an AI-powered chatbot app powered 

# Prequistes:

1) python 3.11+, if you don't have python installed, install it on the 
2) nodejs, if you don't have python installed, install it on the 

## Backend setup (Python)

1) Navaga

Set up virtual environment. Run in terminal:

```
python -m venv .venv 

```

2) Activate the environment 

```
.venv/Scripts/activate
```

3) Install python packages 

```
python -m venv .venv 
```

## Frontend setup

### npm modules setup

1）cd to frotnend
2) run npm install 
3) 

## Environment variables setup
1) Go to .env.example
2) Remove chaneg the name of the file to ".env"
3) Go to openrouter and make an account, paste in the API key
4) (Optional) Go to lo


# Running the app
To run the app, you need to start two servers: 
1) Start the backend server 
2) Start frontend development server (click the generates URL to see the frontend)

## Start Backend Server
1) run fastapi dev \backend\main.py

## Start Frontend Server
1) Open a new terminal 
2) cd frontend 
3) run npm run dev 
4) click the url

## Closing the server
1) Fro the backend, kill the terminal to close the server
2) For the frontend, press "Ctrl+C" in the terminal to close ther server. 
KILLING THE TERMINAL DOES NOT TERMINATE THE SERVER.


## Things to work on
1) Improve UI features
    - "blueticks" to represent read messages
    - icon on top to indicated that websocket is connected (ex. bot is online)
    - Settings support dark mode
    - Settings tool toggle "active" conversation mode
    - Support custom backgrounf images/icons 

2) Chat history
    - Trim chat history when it gets too long

3) Better decision making from should_I_talk bot 
    - Feed the a few most recent chat message history to the should_I_talk,
    instead of the entire message 
    - Better prompts to get better behavior 
    - Better system prompts to get better behavior. 
    - Have the bot's personality influence its decisions in just the right extent 

4) Personality
    - Customize bot personality in the UI, forwarding an update to the langraph state (need UI update)

5) Checkpointing, threads, mutli-chat support, database management 
    - Upgrade from in memeory checkpointing to DB checkpointing 
    - Support mutliple chats each running with different thread-ID (need UI update)

4) HUGE PORJECT: Train/finetune custom LLM models for roleplay, decision making
    - Train a specialized model for roleplay (chatbot)
    - Trained a specialized model for assesing conversational cues to decide wheatehr the bot should talk


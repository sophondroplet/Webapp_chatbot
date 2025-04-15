from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from .graph import agentic_flow
from .timer import timer
from pydantic import BaseModel
from langgraph.types import Command
import uuid
from datetime import datetime

app = FastAPI()

# Configure CORS
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInitResponse(BaseModel):
    thread_id: str
    messages: list

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/init", response_model=ChatInitResponse)
async def initialize_app():

    # Initialize a chat and return a thread_id

    thread_id = str(uuid.uuid4())
    messages = [{"type": "assistant", "content": "Backend initalization complete"}]
        
    return {
        "thread_id": thread_id,
        "messages": messages
    }


@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    
    # Accept the websocket connection and check thread_id
    
    await websocket.accept()
    init_data = await websocket.receive_json()
    thread_id = init_data.get("thread_id")
    config = {"configurable": {"thread_id": thread_id}}

    # initalize chat session in langgraph
    # LLM talks first
    
    stream = agentic_flow.astream(
                    {"LLM_thought_latest": {'content':'The user has summoned you, say a welcome message!',
                                            'timestamp':datetime.now()},
                     
                     "user_message_latest": {'content':'',
                                            'timestamp':datetime.now()}                     
                                            },
                    config,
                    stream_mode="custom",
                )
    
    async for chunk in stream:
        await websocket.send_json({
            "type": "chunk",
            "content": chunk + '▌'  # Add cursor indicator
        })

    last_chunk = chunk.rstrip('▌') if chunk else ""
    
    await websocket.send_json({
        "type": "complete",
        "content": last_chunk
    })


    # initialize timer
    
    Timer = timer(websocket=websocket, config=config)
    asyncio.create_task(Timer.monitor_threads())

    # main loop to listen for new messages
    try:
        while True:
            data = await websocket.receive_json()
            user_input = data.get("user_input")

            try:
                # Setup Langgraph async generator
                print('try to stream')
                stream = agentic_flow.astream(
                    Command(resume={
                        'call_reason':'user_input',
                        'call_content':user_input
                    }),
                    config,
                    stream_mode="custom",
                )

                # Call generator and stream each message chunk
                async for chunk in stream:
                    if chunk == 'XXX':
                        print("LLM decided not to talk")
                        
                    else:    
                        await websocket.send_json({
                            "type": "chunk",
                            "content": chunk + "▌"  # Add cursor indicator
                        })
                
                # Send final message without cursor
                if chunk != 'XXX':
                    last_chunk = chunk.rstrip('▌') if chunk else ""
                    await websocket.send_json({
                        "type": "complete",
                        "content": last_chunk
                    })

            except Exception as e:
                print('stream failed')
                break

    except:
        print('stream failed out')
        print("Client disconnected")
    
    finally:
        print('stream failed out')
        await websocket.close()

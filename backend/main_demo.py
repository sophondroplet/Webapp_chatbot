from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from .message_script import MessageScript, DEMO_SCRIPT
import uuid
from pydantic import BaseModel

app = FastAPI()

class ChatInitResponse(BaseModel):
    thread_id: str
    messages: list

# Configure CORS
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/init", response_model=ChatInitResponse)
async def initialize_app():
    thread_id = str(uuid.uuid4())
    messages = []
    return {
        "thread_id": thread_id,
        "messages": messages
    }

@app.websocket("/ws/chat")
async def websocket_demo_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        # Get initial thread_id
        init_data = await websocket.receive_json()
        thread_id = init_data.get("thread_id")
        
        # Create message script
        script = MessageScript(DEMO_SCRIPT)
        
        # Stream messages
        async for chunk in script.stream():
            # Send chunk or message complete signal
            await websocket.send_json({
                **chunk,
                "thread_id": thread_id
            })
            
            # If message requires user input, wait for it
            if chunk["requires_input"]:
                try:
                    user_response = await websocket.receive_json()
                    # You could process the user response here if needed
                except Exception as e:
                    print(f"Error receiving user response: {e}")
                    break
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

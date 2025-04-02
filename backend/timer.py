# orchestrator.py
import asyncio
from datetime import datetime, timedelta

from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from .graph import agentic_flow


class timer:
    def __init__(self, websocket=None, config=None):
        self.idle_threshold = 30  # seconds
        self.refresh_interval = 6  # seconds
        self.websocket = websocket
        self.config = config
        self.active_threads = {}
        self.is_first_run = True
        self.init_timestamp = datetime.now()

    async def monitor_threads(self):
        while True:
            state = agentic_flow.get_state(self.config)
            
            if self.silence_detect(state):
                await self.trigger_agent(state)

            else:
                print(f'idle time not exceeded: {self.time_elapsed_since_last_activity}')
            
            await asyncio.sleep(self.refresh_interval)

    def silence_detect(self, state):

        last_user_activity = state.values['user_message_latest'].get('timestamp', None)
        last_LLM_activity = state.values['LLM_thought_latest'].get('timestamp', None)

        #return time since chat start with user message is null
        if last_user_activity is None or last_LLM_activity is None:
            print("one timestamp not present")
            self.time_elapsed_since_last_activity = datetime.now() - last_LLM_activity

        #return the more recent message if both are present
        else:
            print("both timestamps present")
            latest_source = last_user_activity if last_user_activity >= last_LLM_activity else last_LLM_activity

            self.time_elapsed_since_last_activity = datetime.now() - latest_source
            print(self.time_elapsed_since_last_activity)
        
        
        return (self.time_elapsed_since_last_activity) > timedelta(seconds=self.idle_threshold)
    
    async def trigger_agent(self, state):
        
        print("User idle, trigger agentic chatbot")
        
        stream = agentic_flow.astream(
                Command(resume={
                        'call_reason':'LLM_thought',
                        'call_content':"""User is online and have read your message, 
                                        but has left you on read"""
                        }),
                self.config, 
                stream_mode="custom",
            )

        print(stream)

        if stream is not None:
            try:
                last_chunk = ""  # Initialize last_chunk before the loop
                async for chunk in stream:
                    last_chunk = chunk  # Update last_chunk in each iteration
                    if self.websocket:  # Check if websocket exists
                        await self.websocket.send_json({
                            "type": "chunk",
                            "content": chunk + "▌"  # Add cursor indicator
                        })
                
                # Send final message without cursor
                if self.websocket:  # Check if websocket exists
                    await self.websocket.send_json({
                        "type": "complete",
                        "content": last_chunk.rstrip('▌') if last_chunk else ""
                    })
            except Exception as e:
                print(f"Error in stream processing: {e}")

        return

    async def analyze_convo_context(self, messages):
        # Implement your secondary LLM analysis here
        # Return True/False based on conversation context
        return True


#run langraph
#run UI

#access state from langgraph
#access inputs from UI
#monitor changes to state and inputs from the UI


#when state changes, activate a timer to monitor user idle time
#when UI, activate a timer to monitor user idle time

#if timer exceeds a certain threshold, activate send request to a small LLM to check if follow up is needed

#if follow up is needed, call LLM

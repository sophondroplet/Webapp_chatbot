from __future__ import annotations as _annotations

import asyncio
from datetime import datetime
from langgraph.types import Command     
from app.agents import should_I_talk_agent
import logfire
from app.graph import agentic_flow

async def main():
    config = {"configurable": {"thread_id": "1"}}

    stream = agentic_flow.astream(
                    {"LLM_thought_latest": {'content':'The user has summoned you, say a welcome message!',
                                        'timestamp':datetime.now()}},
                    config,
                    stream_mode="custom",
                )
    async for chunk in stream:
        print(chunk + '▌')  # Add cursor indicator
    
    user_input = input('you: ')
    
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
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())

# 'The user has said something'

# async def main():
#     config = {"configurable": {"thread_id": "1"}}

#     stream = agentic_flow.astream(
#                     {"LLM_thought_latest": {'content':'The user has summoned you, say a welcome message!',
#                                         'timestamp':datetime.now()}},
#                     config,
#                     stream_mode="custom",
#                 )
#     async for chunk in stream:
#         print(chunk + '▌')  # Add cursor indicator
    
#     user_input = input('you: ')
    
#     stream = agentic_flow.astream(
#                     Command(resume={
#                         'call_reason':'user_input',
#                         'call_content':user_input
#                     }),
#                     config,
#                     stream_mode="custom",
#                 )

#     # Call generator and stream each message chunk
#     async for chunk in stream:
#         print(chunk)

# if __name__ == "__main__":
#     asyncio.run(main())

# 'The user has said something'

# async def main():
#     prompt = {f"""
#               user has not responded in a while
            
#               Your peronality:
#               p1: I'm back, what's up?
#               p2: Hey, how are you doing? 
             
#               Conversation history:
              
#                                     """}
    
#     result = await should_I_talk_agent.run(prompt)
#     print(result.data)

# if __name__ == "__main__":
#         asyncio.run(main())
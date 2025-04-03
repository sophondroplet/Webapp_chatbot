from __future__ import annotations as _annotations

import asyncio
from datetime import datetime
from langgraph.types import Command     
import logfire
from ..graph import agentic_flow
import time

async def main():
    config = {"configurable": {"thread_id": "1"}}

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
        print(chunk + '▌')  # Add cursor indicator
    
    user_input = input('you: ')
    
    stream = agentic_flow.astream(
                    Command(resume={
                            'call_reason':'LLM_thought',
                            'call_content':"""User is online and have read your message. 
                            He seems to be a little busy"""
                            }),
                    config, 
                    stream_mode="custom",
                )

    # Call generator and stream each message chunk
    async for chunk in stream:
        print(chunk)


    #Should return false
    #Test what happens after

    while True:

        user_input = input('you: ')

        print('about to send stream')
        stream = agentic_flow.astream(
                        Command(resume={
                                'call_reason':'LLM_thought',
                                'call_content':"""User is online and have read your message. 
                                He seems to have ignored you, please send a follow up"""
                                }),
                        config, 
                        stream_mode="custom",
                    )
        
        async for chunk in stream:
            print("LLM decided not to talk")
    

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
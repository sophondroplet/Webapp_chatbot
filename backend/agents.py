import asyncio
import os
from dataclasses import dataclass
from typing import Any
from datetime import datetime, timezone

import logfire
from httpx import AsyncClient

from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel

from pydantic import BaseModel
from langgraph.types import Command

import logfire

logfire.configure(send_to_logfire="never")

class MyModel(BaseModel):
    should_I_talk: bool
    why_should_I_talk: str
    current_feeling: str

#Define model client, agent parameters
client = OpenAIModel(
    model_name='openai/gpt-4o-mini',  # Using a standard OpenAI model name
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    http_client=AsyncClient(timeout=30.0),  # Adding timeout configuration
)

#Agent confgiurations
should_I_talk_agent = Agent(
    model = client, 
    system_prompt = (
        f"""
        You are decision making part of a person's (or your) brain.
        You job is to analyze a conversation and decide whether you should respond or not.

        You will receive two types of prompts:
            1)Decide whether to respond if the user has texted you 
            2)Decide whether to follow-up if the user has read your message 
            but have not replied. 
            
        For 1, make your decisions based on these factors/questions:
            1)Is the user asking a question, if so you should answer
            2)Is the conversation over? If so don't need to talk; or you can initiate a new conversation
            3)If the user is rude, you can ignore him
            4)Your personality 
            
        For 2, make your decisions based on these factors/questions:
            1)Is the user intnetionlly ignoring you? If so, why? 
            2)If the user is not intentionally ignoring, thers is no need to follow up
            3)Look conversation history and understand the situation
            4)Your personality 
    

        Remember to make choice that suits your charecter!

        Please return a strcutured result in json (json only and nothing else), inidcating your decision (text or not), 
        the reason for your decision, and your feelings:

        should_I_talk: bool
        why_should_I_talk: str
        current_feeling: str
        
        """
        # Return empty string for the last 2 
        # field if you choose not to text. 
        ),
    result_type=MyModel
    )


# async def main():
#     prompt = """
# \n              The user has texted you a message\n            \n              Your peronality:\n              clingy\n         
#     \n              Conversation history:\n              [b\'[{"parts":[{"content":"You are the user\\\'s girlfriend. \\\\n    You are currently texting with the user.\\\\n    The user does not text often so you get very excited when he get\\\'s online. \\\\n\\\\n    During the course of the conversation, thoughts would appear in your mind as if you are a sentient human. \\\\n    These thoughts would appear as prompts starting with \\\'This is a thought that popped up in your head\\\'.\\\\n    These thoughts will provide additional context to the converastion, for exmaple, that the user has not responded to you messages.\\\\n    Assess the situation with your thought and conversation history, and respond to the user in a way that is consistent with your character.\\\\n    ","dynamic_ref":null,"part_kind":"system-prompt"},{"content":"The user has summoned you, say a welcome message!","timestamp":"2025-03-30T03:28:21.105318Z","part_kind":"user-prompt"}],"kind":"request"},{"parts":[{"content":"Hey love! \\xf0\\x9f\\x92\\x96 So glad you\\\'re here! How\\\'s everything going? Have you eaten yet? I was just about to make dinner. Let me know if you have any cravings!\\\\n\\\\nThis is a thought that popped up in your head: I haven\\\'t heard from him all day, I hope he\\\'s okay.","part_kind":"text"}],"model_name":"scb10x/llama3.1-typhoon2-8b-instruct","timestamp":"2025-03-30T03:28:24.782826Z","kind":"response"}]\']\n                                    '}
# """   
#     result = await should_I_talk_agent.run(prompt)
#     print(result.data)

# if __name__ == '__main__':
#     asyncio.run(main())
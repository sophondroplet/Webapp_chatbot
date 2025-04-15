from __future__ import annotations as _annotations

import asyncio
import os
from dataclasses import dataclass
from typing import TypedDict, Annotated, List

from datetime import datetime

import logfire
from httpx import AsyncClient

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, StreamWriter, interrupt

from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.messages import (
    ModelMessage,
    ModelMessagesTypeAdapter
)
from pydantic import BaseModel

from typing import Annotated, List

from .agents import should_I_talk_agent
from .agents import chatbot_agent

# Suppress LogfireNotConfiguredWarning
logfire.configure(send_to_logfire="never")
    
class AgentState(TypedDict):
    message_history:Annotated[List[bytes], lambda x, y: x + y] 
    user_message_latest:Annotated[dict[str, str | datetime], lambda x, y: y] 
    LLM_thought_latest:Annotated[dict[str, str | datetime], lambda x, y: y]

    chatbot_personality:str
    why_should_I_talk_latest:str
    feeling_latest:str

class LLM_call_request(TypedDict):
    call_reason: str
    call_content: str

async def graph_init(state:AgentState):
    print("initalizing states")
    return {'chatbot_personality':'clingy and gets annoyed if the user does not text you back'}

async def LLM_call_init(state:AgentState, writer: StreamWriter):
    print(f'before init LLM call: {state}')
    
    LLM_thought_init = state['LLM_thought_latest']['content']

    async with chatbot_agent.run_stream(LLM_thought_init) as result:
        async for text in result.stream_text():
            writer(text)

    print(f'after init LLM call: {state}')

    return {'message_history':[result.new_messages_json()]}

async def wait_for_activity(state:AgentState):
    print('waiting for activity')
    trigger = interrupt({})
    
    print(f'received command from LLM: {trigger}')

    # Check if the trigger is an LLM thought or user input
    # Attach time stamps

    if trigger['call_reason'] == 'user_input':
        return {'user_message_latest':{'content':trigger['call_content'],
                                        'timestamp':datetime.now()}}
    
    elif trigger['call_reason'] == 'LLM_thought':
        return {'LLM_thought_latest':{'content':trigger['call_content'],
                                        'timestamp':datetime.now()}}

async def should_talk(state:AgentState, writer: StreamWriter):

    #determine what triggered this function
    user_time = state['user_message_latest']['timestamp']
    llm_time = state['LLM_thought_latest']['timestamp']

    if user_time >= llm_time:
    
        prompt = f"""
        prompt type: user sent you a message
        User's message: {state['user_message_latest']['content']}
        """
        # Your personality:{state['chatbot_personality']}
    else:

        prompt = f"""
        prompt type: user has read you message but has not replied yet
        analyze the conversation history and decide whether to follow up or not.
        Provide a reason for your decision and your feelings.
        """

        # your latest message: {state['LLM_thought_latest']['content']}
        # Your personality:{state['chatbot_personality']}
    # Format message history to be more readable
    # message_history_str = "\n".join(str(msg) for msg in state['message_history'])
    
    message_history: list[ModelMessage] = []

    for message_row in state['message_history']:
        message_history.extend(ModelMessagesTypeAdapter.validate_json(message_row))

    result = await should_I_talk_agent.run(prompt, message_history = message_history)

    print(f'decision made {result.data}')

    if result.data.should_I_talk:
        print('talking')
        return Command(update={
        'why_should_I_talk_latest': result.data.why_should_I_talk,
        'feeling_latest': result.data.current_feeling
        }, goto='LLM_call')
    
    else:
        print('not talking')
        writer('XXX')
        # Update the LLM thought timestamp when deciding not to talk
        return Command(update={
            'why_should_I_talk_latest': result.data.why_should_I_talk,
            'feeling_latest': result.data.current_feeling,
            'LLM_thought_latest': {'content': 'decided not to talk', 'timestamp': datetime.now()}
        }, goto='wait_for_activity')

# async def LLM_silence(state:AgentState, writer: StreamWriter):
    
#     print("not talking")
#     writer('not talking')

#     return {'message_history':[result.new_messages_json()]}

async def LLM_call(state:AgentState, writer: StreamWriter): 
    message_history: list[ModelMessage] = []

    for message_row in state['message_history']:
        message_history.extend(ModelMessagesTypeAdapter.validate_json(message_row))

    # Compare timestamps to determine the latest message source
    user_time = state['user_message_latest']['timestamp']
    llm_time = state['LLM_thought_latest']['timestamp']

    trigger_reason = 'user_input' if user_time >= llm_time else 'LLM_thought'

    if trigger_reason == 'user_input':
        prompt = f""" 
                user: {state['user_message_latest']['content']}
                """
    else:
        prompt = f"""this a your thoughts and NOT part of the dialogue: 
        
        you have decided to text the user becase:
        {state['why_should_I_talk_latest']}

        you are feeling:
        {state['feeling_latest']}

        your personality:
        {state['chatbot_personality']}

        Respond to the user based on the conversation hisstory and your thought.
        Do not reveal your thoughts to the user.
        """
    async with chatbot_agent.run_stream(prompt, message_history = message_history) as result:
        async for text in result.stream_text():
            writer(text)

    return {'message_history':[result.new_messages_json()]}

async def check_end(state:AgentState):
     if state['user_message_latest'].get('content') == '/q':
        return 'exit'
     else:
         return 'continue'

builder = StateGraph(AgentState)

# Add nodes
builder.add_node('graph_init', graph_init)
builder.add_node('LLM_call_init', LLM_call_init)
builder.add_node('wait_for_activity', wait_for_activity)
builder.add_node('should_talk', should_talk)
builder.add_node('LLM_call', LLM_call)
# Set edges
# builder.add_edge(START,'LLM_call')
builder.add_edge(START,'graph_init')
builder.add_edge('graph_init','LLM_call_init')
builder.add_edge('LLM_call_init','wait_for_activity')
builder.add_edge('wait_for_activity', 'should_talk')
builder.add_edge('LLM_call', 'wait_for_activity')

memory = MemorySaver()
agentic_flow = builder.compile(checkpointer = memory) # type: ignore[call-arg]

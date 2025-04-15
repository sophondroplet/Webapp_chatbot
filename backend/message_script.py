from typing import List, Dict, AsyncGenerator, Any
import asyncio

class MessageScript:
    def __init__(self, messages: List[Dict[str, Any]]):
        """
        Initialize with a list of message dictionaries.
        Each message should have format:
        {
            "content": "Your message here",
            "chunk_size": 3,  # Optional: number of words per chunk
            "chunk_delay": 0.2,  # Optional: delay between chunks in seconds
            "end_delay": 1,  # Optional: delay after message completes
            "wait_for_user": False  # Optional: whether to wait for user input
        }
        """
        self.raw_messages = messages
        self._set_defaults()

    def _set_defaults(self):
        """Set default values for optional parameters"""
        for msg in self.raw_messages:
            msg.setdefault("chunk_size", 3)  # words per chunk
            msg.setdefault("chunk_delay", 0.2)
            msg.setdefault("end_delay", 1)
            msg.setdefault("wait_for_user", False)

    def _split_into_chunks(self, text: str, chunk_size: int) -> List[str]:
        """Split text into chunks of specified word size, maintaining cumulative content"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[:i + chunk_size])
            chunks.append(chunk)
        return chunks

    async def stream(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream the messages with appropriate delays and user interaction points.
        Yields dictionaries with format:
        {
            "type": "chunk" | "complete",
            "content": "Cumulative message content so far",
            "requires_input": bool
        }
        """
        for message in self.raw_messages:
            chunks = self._split_into_chunks(message["content"], message["chunk_size"])
            
            # Stream each chunk except the last one
            for chunk in chunks[:-1]:
                yield {
                    "type": "chunk",
                    "content": chunk + "▌",  # Add cursor indicator
                    "requires_input": False
                }
                await asyncio.sleep(message["chunk_delay"])
            
            # Send final chunk with complete type
            if chunks:
                yield {
                    "type": "complete",
                    "content": chunks[-1],  # final content without cursor
                    "requires_input": message["wait_for_user"]
                }
            
            # Wait end delay if specified
            if message["end_delay"] > 0:
                await asyncio.sleep(message["end_delay"])

# Example usage
DEMO_SCRIPT = [
    {
        "content": "Hey! How are you doing today?",
        "chunk_size": 2,
        "chunk_delay": 0.2,
        "end_delay": 1,
        "wait_for_user": True
    },
    {
        "content": "That's great to hear! I'm an AI assistant designed to help answer your questions.",
        "chunk_size": 3,
        "chunk_delay": 0.15,
        "end_delay": 4,
        "wait_for_user": False
    },
    {
        "content": "I can help you with coding, general knowledge, or just casual conversation. What would you like to discuss?",
        "chunk_size": 4,
        "chunk_delay": 0.1,
        "end_delay": 1,
        "wait_for_user": True
    }
]

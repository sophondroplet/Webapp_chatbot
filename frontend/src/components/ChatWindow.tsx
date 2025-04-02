import { useState, useRef, useEffect } from 'react';
import { Message } from '../types';

interface ChatWindowProps {
  websocket: React.RefObject<WebSocket | null>;
  message_history: Message[];
  setMessage_history: React.Dispatch<React.SetStateAction<Message[]>>;
  threadId: string;
}

const ChatWindow: React.FC<ChatWindowProps> = ({
  websocket,
  message_history,
  setMessage_history,
}) => {
  const [inputMessage, setInputMessage] = useState('');
  const messageEndRef = useRef<HTMLDivElement>(null);


  //auto scroll
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [message_history]);

  //handle submit
  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!inputMessage.trim()) return;

    // Add user message
    const userMessage: Message = { 
      content: inputMessage, 
      type: 'user'
    };
    setMessage_history(prev => [...prev, userMessage]);
    
    // Send message to backend
    if (websocket.current?.readyState === WebSocket.OPEN) {
      websocket.current.send(JSON.stringify({
        user_input: inputMessage
      }));
    }

    setInputMessage('');
  };

  return (
    <div className="flex flex-col w-full h-full">
      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {message_history.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[90%] p-4 rounded-xl text-left ${
                  message.type === 'user'
                    ? 'bg-red-400 text-white'
                    : 'bg-white shadow-sm border border-gray-100'
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}
          <div ref={messageEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="bg-white px-4 py-4">
        <form 
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmit();
          }}
          className="max-w-3xl mx-auto flex gap-4 items-center"
        >
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type something..."
            className="flex-1 p-3 rounded-xl bg-gray-200 focus:outline-none"
            autoFocus
          />
          <button
            type="submit"
            className="px-4 !py-3 rounded-xl !bg-red-500 text-white hover:!bg-red-300 transition-colors focus:!outline-none"
          >
            Submit
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatWindow;
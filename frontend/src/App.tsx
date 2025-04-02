import { useState, useRef, useEffect} from 'react';
import './App.css';
import ChatWindow from './components/ChatWindow';
import Modal from './components/Modal';
import { Message } from './types';
import { FiSettings, FiMenu, FiPlus } from 'react-icons/fi';

function App() {
  const [message_history, setMessage_history] = useState<Message[]>([]);
  const [threadId, setThreadId] = useState('');
  const websocket = useRef<WebSocket | null>(null);
  const [isSidebarExpanded, setIsSidebarExpanded] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isNewChatOpen, setIsNewChatOpen] = useState(false);
  const initialized = useRef(false);
  

  // Initialize client, notifies server to create a new thread
  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;

    const initializeChat = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/init', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        const data = await response.json();
        setThreadId(data.thread_id);
        setMessage_history(data.messages);
      } catch (error) {
        console.error('Initialization error:', error);
      }
    };

    initializeChat();
  }, []);

  // WebSocket connection

  useEffect(() => {
    if (!threadId) return;

    const ws = new WebSocket('ws://localhost:8000/chat/ws');
    websocket.current = ws;
    
    ws.onopen = () => {
      ws.send(JSON.stringify({ thread_id: threadId }));
      console.log('WebSocket connected');
    };

    ws.onmessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data);
      if (data.type === 'chunk') {
        setMessage_history(prev => {
          const lastMessage = prev[prev.length - 1];
          if (lastMessage?.type === 'assistant' && !lastMessage.isComplete) {
            const newMessages = [...prev];
            newMessages[prev.length - 1] = {
              ...lastMessage,
              content: data.content
            };
            return newMessages;
          } else {
            return [...prev, { type: 'assistant', content: data.content, isComplete: false }];
          }
        });
      } else if (data.type === 'complete') {
        setMessage_history(prev => {
          const newMessages = [...prev];
          const lastMessage = newMessages[prev.length - 1];
          if (lastMessage?.type === 'assistant') {
            newMessages[prev.length - 1] = {
              ...lastMessage,
              content: data.content,
              isComplete: true
            };
          }
          return newMessages;
        });
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return;
  }, [threadId]);

  return (
    <div className="fixed inset-0 flex">
      {/* Sidebar */}
      <div 
        className={`h-full bg-white shadow-lg transition-all duration-300 flex flex-col ${
          isSidebarExpanded ? 'w-64' : 'w-16'
        }`}
      >
        {/* Menu Button - Always visible */}
        <div className="p-0.1">
          <button
            onClick={() => setIsSidebarExpanded(!isSidebarExpanded)}
            className="w-full flex items-center justify-center hover:bg-gray-100 rounded-lg p-2 transition-colors"
          >
            <FiMenu className="w-6 h-6 text-gray-600" />
          </button>
        </div>
        
        {/* Navigation Buttons */}
        <div className="flex-1">
          {isSidebarExpanded ? (
            <>
              <button
                onClick={() => setIsNewChatOpen(true)}
                className="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-100 transition-colors"
              >
                <FiPlus className="w-5 h-5" />
                <span>New Chat</span>
              </button>
              <button
                onClick={() => setIsSettingsOpen(true)}
                className="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-100 transition-colors"
              >
                <FiSettings className="w-5 h-5" />
                <span>Settings</span>
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => setIsNewChatOpen(true)}
                className="w-full flex items-center justify-center p-4 hover:bg-gray-100 transition-colors"
              >
                <FiPlus className="w-6 h-6 text-gray-600" />
              </button>
              <button
                onClick={() => setIsSettingsOpen(true)}
                className="w-full flex items-center justify-center p-4 hover:bg-gray-100 transition-colors"
              >
                <FiSettings className="w-6 h-6 text-gray-600" />
              </button>
            </>
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex">
        <ChatWindow 
          message_history={message_history} 
          setMessage_history={setMessage_history} 
          threadId={threadId} 
          websocket={websocket}
        />
      </div>

      {/* Modals */}
      <Modal isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />
      <Modal isOpen={isNewChatOpen} onClose={() => setIsNewChatOpen(false)} />
    </div>
  );
}

export default App;

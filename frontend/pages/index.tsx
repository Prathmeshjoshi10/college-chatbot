import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import Head from 'next/head';

// Define types
interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface Source {
  content: string;
  metadata: {
    source: string;
    [key: string]: any;
  };
}

export default function Home() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sources, setSources] = useState<Source[]>([]);
  const [showSources, setShowSources] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setSources([]);

    try {
      // Format chat history for API
      const chatHistory = messages.map((msg) => ({
        role: msg.role,
        content: msg.content,
      }));

      // Call API
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: userMessage.content,
        chat_history: chatHistory,
      });

      // Add assistant message
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);

      // Set sources if available
      if (response.data.sources && response.data.sources.length > 0) {
        setSources(response.data.sources);
      }
    } catch (error) {
      console.error('Error calling API:', error);
      // Add error message
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, there was an error processing your request. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <Head>
        <title>College Chatbot</title>
        <meta name="description" content="Chat with your college assistant" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Header */}
      <header className="bg-blue-600 text-white p-4 shadow-md">
        <div className="container mx-auto">
          <h1 className="text-2xl font-bold">College Chatbot</h1>
          <p className="text-sm">Powered by Google Gemini</p>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-grow container mx-auto p-4 flex flex-col">
        {/* Chat messages */}
        <div className="flex-grow bg-white rounded-lg shadow-md p-4 mb-4 overflow-y-auto max-h-[calc(100vh-250px)]">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-gray-500">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-12 w-12 mb-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
              <p className="text-lg">Ask me anything about the college!</p>
              <p className="text-sm mt-2">Examples:</p>
              <ul className="text-sm mt-1 list-disc list-inside">
                <li>What are the admission requirements?</li>
                <li>How much is the tuition fee?</li>
                <li>What courses are offered?</li>
                <li>Tell me about the campus facilities</li>
              </ul>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                className={`mb-4 ${
                  message.role === 'user' ? 'text-right' : 'text-left'
                }`}
              >
                <div
                  className={`inline-block p-3 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            ))
          )}
          {isLoading && (
            <div className="text-left mb-4">
              <div className="inline-block p-3 rounded-lg bg-gray-200 text-gray-800">
                <div className="flex items-center">
                  <div className="dot-typing"></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Sources */}
        {sources.length > 0 && (
          <div className="mb-4">
            <button
              onClick={() => setShowSources(!showSources)}
              className="text-blue-600 text-sm flex items-center"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className={`h-4 w-4 mr-1 transform ${
                  showSources ? 'rotate-90' : ''
                }`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5l7 7-7 7"
                />
              </svg>
              {showSources ? 'Hide Sources' : 'Show Sources'}
            </button>
            {showSources && (
              <div className="mt-2 p-3 bg-gray-100 rounded-lg text-sm">
                <h3 className="font-bold mb-2">Sources:</h3>
                {sources.map((source, index) => (
                  <div key={index} className="mb-2 pb-2 border-b border-gray-300 last:border-0">
                    <p className="text-gray-800">{source.content.substring(0, 150)}...</p>
                    <p className="text-xs text-gray-500 mt-1">
                      Source: {source.metadata.source}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Input form */}
        <form onSubmit={handleSubmit} className="flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about the college..."
            className="flex-grow p-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="bg-blue-600 text-white p-2 rounded-r-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-blue-400"
            disabled={isLoading || !input.trim()}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
              />
            </svg>
          </button>
        </form>
      </main>

      {/* Footer */}
      <footer className="bg-gray-200 p-4 text-center text-gray-600 text-sm">
        <p>© {new Date().getFullYear()} College Chatbot</p>
      </footer>

      {/* CSS for loading animation */}
      <style jsx>{`
        .dot-typing {
          position: relative;
          left: -9999px;
          width: 10px;
          height: 10px;
          border-radius: 5px;
          background-color: #6b7280;
          color: #6b7280;
          box-shadow: 9984px 0 0 0 #6b7280, 9999px 0 0 0 #6b7280,
            10014px 0 0 0 #6b7280;
          animation: dot-typing 1.5s infinite linear;
        }

        @keyframes dot-typing {
          0% {
            box-shadow: 9984px 0 0 0 #6b7280, 9999px 0 0 0 #6b7280,
              10014px 0 0 0 #6b7280;
          }
          16.667% {
            box-shadow: 9984px -10px 0 0 #6b7280, 9999px 0 0 0 #6b7280,
              10014px 0 0 0 #6b7280;
          }
          33.333% {
            box-shadow: 9984px 0 0 0 #6b7280, 9999px 0 0 0 #6b7280,
              10014px 0 0 0 #6b7280;
          }
          50% {
            box-shadow: 9984px 0 0 0 #6b7280, 9999px -10px 0 0 #6b7280,
              10014px 0 0 0 #6b7280;
          }
          66.667% {
            box-shadow: 9984px 0 0 0 #6b7280, 9999px 0 0 0 #6b7280,
              10014px 0 0 0 #6b7280;
          }
          83.333% {
            box-shadow: 9984px 0 0 0 #6b7280, 9999px 0 0 0 #6b7280,
              10014px -10px 0 0 #6b7280;
          }
          100% {
            box-shadow: 9984px 0 0 0 #6b7280, 9999px 0 0 0 #6b7280,
              10014px 0 0 0 #6b7280;
          }
        }
      `}</style>
    </div>
  );
}

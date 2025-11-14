import React from 'react';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';
import { useChat } from '../../hooks/useChat';

export default function ChatInterface() {
  const { messages, isLoading, sendMessage } = useChat();

  return (
    <div className="flex-1 max-w-5xl mx-auto w-full px-4 py-4 sm:py-8 flex flex-col h-[calc(100vh-70px)] sm:h-[calc(100vh-80px)]">
      <div className="flex-1 overflow-y-auto mb-4 sm:mb-6 space-y-3 sm:space-y-4">
        {messages.map((message, index) => (
          <MessageBubble key={index} message={message} />
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="w-8 h-8 sm:w-10 sm:h-10 bg-red-600 rounded-full flex items-center justify-center mr-2 sm:mr-3">
              <span className="text-white text-sm font-bold">A</span>
            </div>
            <div className="bg-white rounded-2xl px-4 py-3 sm:px-6 sm:py-4 border border-gray-200">
              <div className="flex gap-1 sm:gap-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay:'0.1s'}}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay:'0.2s'}}></div>
              </div>
            </div>
          </div>
        )}
      </div>
      <ChatInput onSendMessage={sendMessage} isLoading={isLoading} />
    </div>
  );
}
import React, { useState } from 'react';
import { Send } from 'lucide-react';

export default function ChatInput({ onSendMessage, isLoading }) {
  const [inputMessage, setInputMessage] = useState('');

  const handleSend = () => {
    if (inputMessage.trim() && !isLoading) {
      onSendMessage(inputMessage);
      setInputMessage('');
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-3 sm:p-4 flex items-center gap-2 sm:gap-3">
      <input
        type="text"
        value={inputMessage}
        onChange={(e) => setInputMessage(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        placeholder="Задайте ваш вопрос..."
        className="flex-1 outline-none text-gray-900 placeholder-gray-400 text-sm sm:text-base"
        disabled={isLoading}
      />
      <button
        onClick={handleSend}
        disabled={isLoading || !inputMessage.trim()}
        className="bg-red-400 hover:bg-red-500 text-white rounded-xl p-2 sm:p-3 transition disabled:opacity-50"
      >
        <Send size={18} className="sm:size-20" />
      </button>
    </div>
  );
}
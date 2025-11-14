import React from 'react';

export default function MessageBubble({ message }) {
  return (
    <div className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
      {message.role === 'assistant' && (
        <div className="w-8 h-8 sm:w-10 sm:h-10 bg-red-600 rounded-full flex items-center justify-center mr-2 sm:mr-3 flex-shrink-0">
          <span className="text-white text-xs sm:text-sm font-bold">A</span>
        </div>
      )}
      <div className={`max-w-xs sm:max-w-sm md:max-w-md lg:max-w-2xl rounded-2xl px-4 py-3 sm:px-6 sm:py-4 ${
        message.role === 'user' ? 'bg-red-600 text-white' : 'bg-white text-gray-900 border border-gray-200'
      }`}>
        <p className="whitespace-pre-wrap text-sm sm:text-base">{message.content}</p>
      </div>
    </div>
  );
}
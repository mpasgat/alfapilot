import React from 'react';
import { MessageSquare } from 'lucide-react';

export default function Header({ currentView, onNavigate }) {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center gap-2 sm:gap-3">
          <div className="w-8 h-8 sm:w-10 sm:h-10 bg-red-600 rounded-full flex items-center justify-center">
            <span className="text-white font-bold text-lg sm:text-xl">A</span>
          </div>
          <h1 className="text-lg sm:text-xl font-bold text-gray-900">БизнесАссистент</h1>
        </div>
        <nav className="flex items-center gap-4 sm:gap-6">
          <button
            onClick={currentView === 'chat' ? onNavigate : undefined}
            className="text-gray-600 hover:text-gray-900 transition text-sm sm:text-base"
          >
            Главная
          </button>
          <button
            onClick={currentView === 'home' ? onNavigate : undefined}
            className="bg-red-600 text-white px-3 py-2 sm:px-6 sm:py-2 rounded-lg font-medium hover:bg-red-700 transition flex items-center gap-1 sm:gap-2 text-sm sm:text-base"
          >
            <MessageSquare size={16} className="sm:block" />
            <span className="hidden sm:inline">Консультация</span>
            <span className="sm:hidden">Чат</span>
          </button>
        </nav>
      </div>
    </header>
  );
}
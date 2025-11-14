import React from 'react';
import { Sparkles } from 'lucide-react';

export default function HeroSection({ onStartConsultation }) {
  return (
    <section className="max-w-7xl mx-auto px-4 py-12 sm:py-20 text-center">
      <div className="inline-flex items-center gap-2 bg-red-50 text-red-600 px-3 py-1 sm:px-4 sm:py-2 rounded-full mb-6 sm:mb-8">
        <Sparkles size={16} className="sm:size-18" />
        <span className="font-medium text-sm sm:text-base">Powered by AI</span>
      </div>
      
      <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-900 mb-4 sm:mb-6">
        Умный помощник для вашего<br />бизнеса
      </h2>
      
      <p className="text-base sm:text-lg md:text-xl text-gray-600 mb-8 sm:mb-10 max-w-3xl mx-auto">
        Получайте экспертные рекомендации по ключевым вопросам<br className="hidden sm:inline" />
        бизнеса с использованием искусственного интеллекта
      </p>
      
      <div className="flex flex-col sm:flex-row gap-4 sm:gap-4 justify-center">
        <button
          onClick={onStartConsultation}
          className="bg-red-600 text-white px-6 py-3 sm:px-8 sm:py-4 rounded-lg font-medium text-base sm:text-lg hover:bg-red-700 transition w-full sm:w-auto"
        >
          Начать консультацию
        </button>
        <button className="bg-white text-gray-700 px-6 py-3 sm:px-8 sm:py-4 rounded-lg font-medium text-base sm:text-lg hover:bg-gray-50 transition border border-gray-300 w-full sm:w-auto">
          Узнать больше
        </button>
      </div>
    </section>
  );
}
import React from 'react';

export default function ConsultationCard({ area, onClick }) {
  // Add defensive check for area prop
  if (!area) {
    return null;
  }
  
  const Icon = area.icon;
  
  return (
    <div
      className="bg-white rounded-xl p-5 sm:p-6 border border-gray-200 hover:shadow-lg transition cursor-pointer h-full"
      onClick={onClick}
    >
      <div className={`${area.color} w-12 h-12 sm:w-14 sm:h-14 rounded-xl flex items-center justify-center mb-4`}>
        {/* Render icon if it exists */}
        {Icon ? <Icon className="text-red-600" size={24} /> : 
         <div className="w-6 h-6 bg-gray-400 rounded-full"></div>}
      </div>
      <h4 className="text-lg sm:text-xl font-bold text-gray-900 mb-3">{area.title}</h4>
      <p className="text-gray-600 text-sm sm:text-base mb-5 sm:mb-6">{area.description}</p>
      <button className="text-red-600 font-medium hover:text-red-700 transition flex items-center gap-2 text-sm">
        Получить консультацию <span>→</span>
      </button>
    </div>
  );
}
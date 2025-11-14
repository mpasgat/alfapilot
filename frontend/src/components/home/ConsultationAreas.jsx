import React from 'react';
import ConsultationCard from './ConsultationCard';
import { 
  Megaphone, 
  FileText, 
  Scale, 
  TrendingUp 
} from 'lucide-react';

const consultationAreas = [
  {
    id: 'marketing',
    title: 'Маркетинг',
    description: 'Создание продающих постов для соцсетей и рекламных материалов',
    color: 'bg-blue-100',
    icon: Megaphone
  },
  {
    id: 'documents',
    title: 'Документы',
    description: 'Подготовка деловых писем, коммерческих предложений и других документов',
    color: 'bg-green-100',
    icon: FileText
  },
  {
    id: 'legal',
    title: 'Юридические услуги',
    description: 'Анализ договоров и выявление потенциальных рисков',
    color: 'bg-purple-100',
    icon: Scale
  },
  {
    id: 'finance',
    title: 'Финансы',
    description: 'Финансовый анализ и прогнозирование денежных потоков',
    color: 'bg-yellow-100',
    icon: TrendingUp
  }
];

export default function ConsultationAreas({ onStartConsultation }) {
  return (
    <section className="py-12 sm:py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12 sm:mb-16">
          <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 mb-3 sm:mb-4">
            Наши направления консультаций
          </h2>
          <p className="text-base sm:text-xl text-gray-600 max-w-3xl mx-auto px-2">
            Получите профессиональную помощь в различных аспектах вашего бизнеса
          </p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
          {consultationAreas.map((area) => (
            <ConsultationCard 
              key={area.id} 
              area={area} 
              onClick={() => onStartConsultation(area.id)} 
            />
          ))}
        </div>
      </div>
    </section>
  );
}
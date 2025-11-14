import { Scale, TrendingUp, DollarSign, Users, Settings } from 'lucide-react';

export const CONSULTATION_AREAS = [
  {
    id: 'legal',
    title: 'Юридические вопросы',
    description: 'Консультации по договорам, лицензированию, трудовому праву и защите интеллектуальной собственности',
    icon: Scale,
    color: 'bg-red-50'
  },
  {
    id: 'marketing',
    title: 'Маркетинг и продажи',
    description: 'Стратегии продвижения, анализ рынка, SMM, контент-маркетинг и увеличение продаж',
    icon: TrendingUp,
    color: 'bg-red-50'
  },
  {
    id: 'finance',
    title: 'Финансы и бухгалтерия',
    description: 'Планирование бюджета, налоговая оптимизация, управление денежными потоками',
    icon: DollarSign,
    color: 'bg-red-50'
  },
  {
    id: 'hr',
    title: 'Управление персоналом',
    description: 'Найм сотрудников, мотивация команды, корпоративная культура и развитие персонала',
    icon: Users,
    color: 'bg-red-50'
  },
  {
    id: 'operations',
    title: 'Операционная деятельность',
    description: 'Оптимизация процессов, автоматизация, логистика и управление качеством',
    icon: Settings,
    color: 'bg-red-50'
  }
];

export const INITIAL_MESSAGE = {
  role: 'assistant',
  content: 'Здравствуйте! Я ваш AI-ассистент для малого бизнеса. Чем могу помочь сегодня? Я могу проконсультировать по вопросам юриспруденции, маркетинга, финансов, управления персоналом и операционной деятельности.'
};
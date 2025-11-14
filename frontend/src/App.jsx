import React, { useState } from 'react';
import Header from './components/layout/Header';
import HeroSection from './components/home/HeroSection';
import ConsultationAreas from './components/home/ConsultationAreas';
import ChatInterface from './components/chat/ChatInterface';

export default function App() {
  const [currentView, setCurrentView] = useState('home');

  return (
    <div className="min-h-screen bg-gray-50">
      {currentView === 'home' ? (
        <>
          <Header currentView={currentView} onNavigate={() => setCurrentView('chat')} />
          <main>
            <HeroSection onStartConsultation={() => setCurrentView('chat')} />
            <ConsultationAreas onStartConsultation={() => setCurrentView('chat')} />
          </main>
        </>
      ) : (
        <>
          <Header currentView={currentView} onNavigate={() => setCurrentView('home')} />
          <ChatInterface />
        </>
      )}
    </div>
  );
}
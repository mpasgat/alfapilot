// API base URL - works both in Docker and local development
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

// Helper function to get welcome message with hints
export function getWelcomeMessage() {
  return `👋 Добро пожаловать в Alfapilot!

Я помогу вам с различными задачами. Вот что я умею:

📊 **Финансы**: Используйте слова "финансы", "бюджет", "расходы", "доходы", "налоги"
📝 **Документы**: Используйте слова "документ", "письмо", "заявление", "операционная деятельность"
⚖️ **Юриспруденция**: Используйте слова "юридический", "договор", "персонал", "кадры", "право"
📣 **Маркетинг**: Любые другие запросы будут обработаны как маркетинговые

Просто напишите ваш запрос, и я автоматически направлю его к нужному специалисту!`;
}

// Generic chat function - routes to appropriate endpoint based on message
export async function sendMessageToBackend(messages) {
  try {
    // Extract the last user message
    const lastMessage = messages[messages.length - 1];
    const userText = (lastMessage.content || lastMessage).toLowerCase();
    
    // Detect intent from user message with expanded keyword lists
    let endpoint = '/marketing/generate-posts';
    let requestBody = {
      idea: lastMessage.content || lastMessage,
      tone: "professional",
      target_audience: "general"
    };
    
    // Check for finance keywords (расширенный список)
    const financeKeywords = ['финанс', 'бюджет', 'расход', 'доход', 'прибыль', 'убыток', 
                             'бухгалтер', 'налог', 'отчет', 'баланс', 'аналит',
                             'finance', 'budget', 'accounting', 'tax', 'profit', 'revenue'];
    if (financeKeywords.some(keyword => userText.includes(keyword))) {
      endpoint = '/finance/analyze-data';
      requestBody = {
        data: lastMessage.content || lastMessage,
        analysis_type: "general"
      };
    }
    // Check for legal keywords (расширенный список)
    else if (userText.includes('юрид') || userText.includes('юрист') || 
             userText.includes('договор') || userText.includes('контракт') || 
             userText.includes('право') || userText.includes('закон') ||
             userText.includes('иск') || userText.includes('суд') ||
             userText.includes('персонал') || userText.includes('кадр') || userText.includes('сотрудник') ||
             userText.includes('legal') || userText.includes('contract') || userText.includes('law') ||
             userText.includes('compliance') || userText.includes('regulation')) {
      endpoint = '/legal/analyze-contract';
      requestBody = {
        contract_text: lastMessage.content || lastMessage,
        analyze_risks: true
      };
    }
    // Check for document keywords (расширенный список)
    else if (userText.includes('документ') || userText.includes('письмо') || 
             userText.includes('заявлен') || userText.includes('запрос') ||
             userText.includes('бланк') || userText.includes('форм') || userText.includes('шаблон') ||
             userText.includes('операцион') || userText.includes('деятельность') ||
             userText.includes('document') || userText.includes('letter') || 
             userText.includes('template') || userText.includes('form')) {
      endpoint = '/documents/generate-document';
      requestBody = {
        doc_type: "letter",
        content: lastMessage.content || lastMessage,
        style: "formal"
      };
    }
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      throw new Error(`Backend API Error: ${response.status}`);
    }

    const data = await response.json();
    // Format response based on endpoint type
    let responseText = '';
    
    if (data.post_variants) {
      // Marketing response
      responseText = data.post_variants.join('\n\n---\n\n');
      if (data.suggestions && data.suggestions.length > 0) {
        responseText += '\n\n📝 Рекомендации:\n' + data.suggestions.map(s => '• ' + s).join('\n');
      }
    } else if (data.document) {
      // Document response
      responseText = data.document;
      if (data.suggestions && data.suggestions.length > 0) {
        responseText += '\n\n📝 Рекомендации:\n' + data.suggestions.map(s => '• ' + s).join('\n');
      }
    } else if (data.summary) {
      // Legal response
      responseText = '📋 Резюме:\n' + data.summary;
      if (data.risks && data.risks.length > 0) {
        responseText += '\n\n⚠️ Риски:\n' + data.risks.map(r => '• ' + r).join('\n');
      }
      if (data.recommendations && data.recommendations.length > 0) {
        responseText += '\n\n✅ Рекомендации:\n' + data.recommendations.map(r => '• ' + r).join('\n');
      }
    } else if (data.analysis) {
      // Finance response
      responseText = '💰 Анализ:\n' + data.analysis;
      if (data.recommendations && data.recommendations.length > 0) {
        responseText += '\n\n✅ Рекомендации:\n' + data.recommendations.map(r => '• ' + r).join('\n');
      }
    } else {
      responseText = 'Ответ получен';
    }
    
    return responseText;
  } catch (error) {
    console.error('Error calling backend API:', error);
    throw error;
  }
}

// Marketing API functions
export async function sendMarketingRequest(idea, tone = "professional", target_audience = "general") {
  try {
    const response = await fetch(`${API_BASE_URL}/marketing/generate-posts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        idea: idea,
        tone: tone,
        target_audience: target_audience
      })
    });

    if (!response.ok) {
      throw new Error(`Backend API Error: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error calling marketing API:', error);
    throw error;
  }
}

// Documents API
export async function generateDocument(docType, content, style = "formal") {
  try {
    const response = await fetch(`${API_BASE_URL}/documents/generate-document`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        doc_type: docType,
        content: content,
        style: style
      })
    });

    if (!response.ok) {
      throw new Error(`Backend API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error calling documents API:', error);
    throw error;
  }
}

// Legal API
export async function analyzeContract(contractText, analyzeRisks = true) {
  try {
    const response = await fetch(`${API_BASE_URL}/legal/analyze-contract`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contract_text: contractText,
        analyze_risks: analyzeRisks
      })
    });

    if (!response.ok) {
      throw new Error(`Backend API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error calling legal API:', error);
    throw error;
  }
}

// Finance API
export async function analyzeFinanceData(data, analysisType = "summary") {
  try {
    const response = await fetch(`${API_BASE_URL}/finance/analyze-data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        data: data,
        analysis_type: analysisType
      })
    });

    if (!response.ok) {
      throw new Error(`Backend API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error calling finance API:', error);
    throw error;
  }
}

// Health check
export async function checkBackendHealth() {
  try {
    const response = await fetch('/api/health');
    return response.ok;
  } catch (error) {
    console.error('Backend health check failed:', error);
    return false;
  }
}
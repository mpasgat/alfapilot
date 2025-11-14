// Updated to connect to the existing backend API instead of Anthropic directly
export async function sendMessageToBackend(messages) {
  try {
    // Send the message to our backend which will route it to the appropriate AI service
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: messages
      })
    });

    if (!response.ok) {
      throw new Error(`Backend API Error: ${response.status}`);
    }

    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error('Error calling backend API:', error);
    throw error;
  }
}

// We need to add a new endpoint to the backend for this chat functionality
// For now, we'll create a simple function that routes to the marketing service as an example
export async function sendMarketingRequest(idea, tone = "professional", target_audience = "general") {
  try {
    const response = await fetch('/api/v1/marketing/generate-posts', {
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
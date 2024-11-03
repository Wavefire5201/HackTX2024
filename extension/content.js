// Create the chatbot button
const chatbotButton = document.createElement('div');
chatbotButton.id = 'chatbotButton';
chatbotButton.style.cursor = 'pointer';

const chatbotIcon = document.createElement('img');
chatbotIcon.src = chrome.runtime.getURL(chat.svg);
chatbotIcon.alt = 'Chatbot';
chatbotIcon.style.width = '50px';
chatbotIcon.style.height = '50px';

chatbotButton.appendChild(chatbotIcon);
document.body.appendChild(chatbotButton);

// Add styles and animation for the chatbot
const style = document.createElement('style');
style.textContent = `
  #chatbotButton {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    background-color: #007bff;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 24px;
    transition: transform 0.3s ease;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
  }

  #chatbotContainer {
    display: none;
    position: fixed;
    bottom: 80px;
    right: 20px;
    width: 320px;
    padding: 10px;
    background-color: white;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    animation: slide-in 0.3s ease;
    max-height: 400px;
    overflow-y: hidden;
    font-family: Arial, sans-serif;
  }

  #chatbotContainer.show {
    display: block;
  }

  #chatbotClose {
    display: flex;
    justify-content: flex-end;
    font-size: 16px;
    color: #555;
    cursor: pointer;
  }

  #chatbotHistory {
    margin-top: 10px;
    max-height: 300px;
    overflow-y: auto;
  }

  .chatbotMessage {
    position: relative;
    margin: 8px 0;
    padding: 8px 12px;
    border-radius: 15px;
    font-size: 14px;
    max-width: 70%;
    word-wrap: break-word;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  }

  .userMessage {
    background-color: #007bff;
    color: white;
    text-align: right;
    align-self: flex-end;
    margin-left: auto;
    border-radius: 15px 15px 0px 15px;
  }

  .botMessage {
    background-color: #f1f1f1;
    color: black;
    text-align: left;
    margin-right: auto;
    border-radius: 15px 15px 15px 0px;
  }

  #chatbotInput {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    outline: none;
  }

  @keyframes slide-in {
    from {
      transform: translateY(20px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
`;
document.head.appendChild(style);

// Create the chatbot container and close button
const chatbotContainer = document.createElement('div');
chatbotContainer.id = 'chatbotContainer';

// Close button above chat history
const chatbotClose = document.createElement('div');
chatbotClose.id = 'chatbotClose';
chatbotClose.textContent = '✖';
chatbotContainer.appendChild(chatbotClose);

// Create chatbot history container
const chatbotHistory = document.createElement('div');
chatbotHistory.id = 'chatbotHistory';
chatbotContainer.appendChild(chatbotHistory);

// Create chatbot input field
const chatbotInput = document.createElement('input');
chatbotInput.id = 'chatbotInput';
chatbotInput.placeholder = 'Type your message...';
chatbotContainer.appendChild(chatbotInput);

document.body.appendChild(chatbotContainer);

// Toggle chatbot display on button click with animation
chatbotButton.addEventListener('click', () => {
  chatbotContainer.classList.toggle('show');
});

// Close chatbot on 'X' click
chatbotClose.addEventListener('click', () => {
  chatbotContainer.classList.remove('show');
});

// Handle chatbot responses and history
chatbotInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    const userText = chatbotInput.value.trim();
    if (userText) {
      // Display user's message in the chatbot history
      const userMessage = document.createElement('div');
      userMessage.className = 'chatbotMessage userMessage';
      userMessage.textContent = userText;
      chatbotHistory.appendChild(userMessage);

      // Display bot's response
      const botMessage = document.createElement('div');
      botMessage.className = 'chatbotMessage botMessage';
      botMessage.textContent = `You said: ${userText}`;
      chatbotHistory.appendChild(botMessage);

      // Scroll to the bottom of the chatbot history
      chatbotHistory.scrollTop = chatbotHistory.scrollHeight;

      // Clear the input field
      chatbotInput.value = '';
    }
  }
});

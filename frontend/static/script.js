document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chatBox');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    
    function addMessage(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                if (data.response) {
                    addMessage(data.response, false);
                } else if (data.error) {
                    addMessage("Error: " + data.error, false);
                }
            } catch (error) {
                addMessage("Error connecting to the server", false);
                console.error('Error:', error);
            }
        }
    }
    
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Add welcome message in demo mode
    if (window.location.pathname === '/demo') {
        addMessage("Welcome to the Gemini Chat demo! How can I help you today?", false);
    }
});
import google.generativeai as genai

class GeminiChat:
    def __init__(self):
        self.API_KEY = "AIzaSyBiFSh1arfGoP6S0F6pYZRZJIacBWme4vM"
        genai.configure(api_key=self.API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.chat_session = None

    def start_chat(self):
        self.chat_session = self.model.start_chat()
        return self.chat_session

    def get_response(self, user_input):
        if not self.chat_session:
            self.start_chat()
        response = self.chat_session.send_message(user_input)
        return response.text

# Standalone version (for testing)
def standalone_chat():
    print("Chat with Gemini! Type 'exit' to quit.")
    chat = GeminiChat()
    chat.start_chat()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = chat.get_response(user_input)
        print("Gemini:", response)

if __name__ == "__main__":
    standalone_chat()
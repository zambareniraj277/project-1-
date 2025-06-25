https://github.com/zambareniraj277/project-1-.git
# Gemini Chat App

A simple chat application powered by the Gemini API.

## Prerequisites

- Python 3.6+
- pip
- A Gemini API key

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/zambareniraj277/project-1-.git)
   cd gemini-chat-app
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate.bat  # On Windows
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Set your Gemini API key as an environment variable:

   ```bash
   export GEMINI_API_KEY="YOUR_API_KEY"  # On Linux/macOS
   set GEMINI_API_KEY="YOUR_API_KEY"  # On Windows
   ```

   Replace `YOUR_API_KEY` with your actual Gemini API key.

## Running the Application

1.  Run the backend:

    ```bash
    cd backend
    python main.py
    ```

2.  Run the frontend:

    Open the `frontend/templates/index.html` file in your browser.

## Notes

- The backend runs on Flask.
- The frontend is a simple HTML/CSS/JavaScript application.

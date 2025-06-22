
🤖 SynthMind – AI Chatbot with User Authentication & Chat History

SynthMind is a smart AI chatbot built using Streamlit, Ollama (Gemma 2B model), and MySQL. It supports user registration, login, session-based chat history, and generates real-time responses from a local LLM (Gemma) using Ollama. This chatbot is designed for privacy, speed, and real-world usability.


 🌟 Features

🔐 User Registration & Login
💬 Chat interface with real-time AI responses
🧠 Powered by Gemma 2B LLM running locally via Ollama
💾 Chat history stored session-wise in MySQL database
🖥️ Streamlit-based clean web UI
🔒 No external API – all local and secure


⚙️ Technologies Used

Python 3.x
Streamlit– frontend framework
Ollama– for local LLM interaction (Gemma 2B)
MySQL– user and chat data storage
UUID– for unique session IDs
datetime– to log activity timestamps
logging – for backend debugging


🚀 Installation Guide

🔧 Prerequisites

- Python 3.x installed
- MySQL Server installed (e.g., via XAMPP, WAMP)
- Ollama installed from [https://ollama.com](https://ollama.com)



🛠️ Step-by-Step Setup

1.Clone the Repository
"
git clone https://github.com/YourUsername/SynthMind.git
cd SynthMind
"

2.Install Python Dependencies
"
pip install -r requirements.txt
"

3.Set Up MySQL Database

-Open MySQL and run the SQL script to create tables:
"
CREATE DATABASE synthmind_AI_DB;
USE synthmind_AI_DB;

CREATE TABLE user_data (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(250),
    Age INT,
    Gender VARCHAR(30),
    Country VARCHAR(150),
    City VARCHAR(250),
    UserID VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    RegisteredAt DATETIME
);

CREATE TABLE chat_history (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    UserID VARCHAR(100),
    messege_role ENUM('user', 'assistant'),
    message_content LONGTEXT,
    DateTime DATETIME DEFAULT CURRENT_TIMESTAMP (),
    Session_ID VARCHAR(100),
    Session_Title VARCHAR(250)
);

"
4.Configure Streamlit Secrets

In the `.streamlit/` folder, create a `secrets.toml` file:
[mysql]
host = "localhost"
user = "your_mysql_username"
password = "your_mysql_password"
database = "synthmind_AI_DB"
port = 3306


5. Pull the Gemma Model (with Ollama)

ollama pull gemma:2b



6. Run the App

"
streamlit run app.py
"

Then open the browser URL shown in the terminal (usually http://localhost:8501).


📸 Screenshots

Add interface and chatbot screenshots here after uploading to GitHub._



🧠 Future Scope

- Voice input/output
- Multilingual support
- Emotion-aware AI replies
- Admin dashboard
- Deployment to cloud



 🤝 Contribution

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.



 📄 License

This project is for educational use. Please give credit when sharing or forking.



 🙏 Acknowledgements

Thanks to:
- Streamlit for UI
- Ollama for local LLM support
- Python and MySQL communities

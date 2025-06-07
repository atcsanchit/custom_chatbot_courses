# 🎓 Custom Chatbot for Course Guidance

A personalized AI-powered chatbot designed to assist users in navigating and understanding course content. This project offers tailored responses for each course module, helping learners grasp concepts efficiently through conversation.


![AI Assistant](https://img.shields.io/badge/AI-Assistant-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🧠 Overview

This chatbot simulates an intelligent tutor that can:
- Answer questions related to course material.
- Provide summaries and explanations of topics.
- Assist with doubts in real-time via an interactive UI.

It is built to help students access course-related assistance anytime and is especially useful in self-paced or remote learning environments.


## 🚀 Features

- 🗂️ Supports multiple courses and modules.
- 💬 Natural Language Conversation.
- 🧾 Summarization and breakdown of course content.
- 🔍 Context-aware question answering.
- 🖥️ Interactive web-based UI.


## 🛠 Tech Stack

- **Python** – Core logic and backend.
- **FastAPI** – Backend API service.
- **Langchain / LLM APIs** – For prompt handling and response generation.
- **Streamlit** – Frontend UI for user interaction.
- **ChromaDB / FAISS** – Vector store for semantic search.
- **Mistral** – As the LLM backend (configurable).

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- API keys for AI services (Deepgram, Mistral, etc.)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/atcsanchit/custom_chatbot_courses.git
cd custom_chatbot_courses
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the assistant:
```bash
uvicorn main:app --reload
```

## 📋 Configuration

Create a `.env` file in the root directory with the following variables:

```env
# API Keys
MISTRAL_API_KEY=your_mistral_api_key_here
PORT=your_port_number_here
```

## 🏗️ Project Structure


custom_chatbot_courses/
├── notebook/            # Jupyter notebooks for experimentation
├── src/                 # Source code for core functionalities
├── main.py              # Pipeline script
├── app.py               # Entry point for the application
├── requirements.txt     # Python dependencies
├── setup.py             # Setup script for installation
└── README.md            # Project documentation

```

## 🧰 Tech Stack

- Python
- FastAPI – backend server
- FAISS  – Vector Database
- Mistral / GPT models – LLM response


## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MistralAI for GPT models
- The open-source AI community
- Contributors and testers

## 📞 Support

- **Email**: [atcsanchit@gmail.com](mailto:your-email@example.com)

---

**Made with ❤️ by [Sanchit](https://github.com/atcsanchit)**

*Star ⭐ this repo if you find it helpful!*
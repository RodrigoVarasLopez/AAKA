# 🔑 AAKA AI API Key Analyzer 🕵️‍♂️✨

This web application built with Streamlit automatically identifies which AI platform (OpenAI, DeepSeek, Anthropic) an API key belongs to and provides a quick overview of the available resources on that platform. You can test the app directly at the following link: [AAKA](https://aaka89.streamlit.app/)

## 🚀 Main Features

- 🕵️‍♂️ **Automatic platform identification** from the API key.
- 📋 **List of available models**.
- 🧑‍💻 **Additional details** such as Assistants and Vector Stores (for OpenAI).
- ⚡️ Simple and user-friendly interface.

## 🛠️ Requirements

- Python 3.7 or higher
- A valid API Key from [OpenAI](https://platform.openai.com), [DeepSeek](https://deepseek.com/), or [Anthropic](https://www.anthropic.com/).

## 📥 Installation

1. **Clone** the repository:

```bash
git clone https://github.com/RodrigoVarasLopez/AAKA.git
cd AAKA
```

2. **Install the dependencies:**

```bash
pip install streamlit openai requests
```

## 🏃‍♂️ Run the Application

```bash
streamlit run api_key_analyzer.py
```

A window will automatically open in your browser at `http://localhost:8501`.

## 📖 How to Use

- Enter your **API KEY** in the provided field.
- Click on **"Identify API Platform"**.
- See the identified platform and automatically review the available resources.

## 📦 Supported Platforms

- ✅ OpenAI
- ✅ DeepSeek
- ✅ Anthropic

## 🧑‍💻 Author

Created with ❤️ by [Your Name](https://github.com/yourusername)

## 📜 License

This project is licensed under the MIT License.


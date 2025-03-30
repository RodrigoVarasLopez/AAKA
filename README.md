# 🔑AAKA AI API Key Analyzer 🕵️‍♂️✨

Esta aplicación web, construida con Streamlit, identifica automáticamente a qué plataforma de Inteligencia Artificial pertenece una API Key (OpenAI, DeepSeek, Anthropic) y ofrece un resumen rápido de los recursos disponibles en dicha plataforma.

## 🚀 Características principales

- 🕵️‍♂️ **Identificación automática** de la plataforma a partir de la API Key.
- 📋 **Listado de modelos** disponibles.
- 🧑‍💻 **Detalles adicionales** como Asistentes y Vector Stores (para OpenAI).
- ⚡️ Interfaz sencilla y amigable.

## 🛠️ Herramientas necesarias

- Python 3.7 o superior
- Una API Key válida de [OpenAI](https://platform.openai.com), [DeepSeek](https://deepseek.com/), o [Anthropic](https://www.anthropic.com/).

## 📥 Instalación

1. **Clona** el repositorio:

```bash
git clone https://github.com/RodrigoVarasLopez/AAKA.git
cd AAKA
```

2. **Instala las dependencias:**

```bash
pip install streamlit openai requests
```

## 🏃‍♂️ Ejecuta la aplicación

```bash
streamlit run api_key_analyzer.py
```

Una ventana se abrirá automáticamente en tu navegador con la dirección `http://localhost:8501`.

## 📖 Cómo utilizar la app

- Ingresa tu **API KEY** en el campo proporcionado.
- Haz clic en **"Identify API Platform"**.
- Observa la plataforma identificada y revisa los recursos disponibles automáticamente.

## 📦 Plataformas soportadas

- ✅ OpenAI
- ✅ DeepSeek
- ✅ Anthropic

## 🧑‍💻 Autor

Creado con ❤️ por [Tu Nombre](https://github.com/tuusuario)

## 📜 Licencia

Este proyecto está bajo licencia MIT.

import streamlit as st
import openai
import requests

# App Title and Description
st.title("🔑 AAKA AI API Key Analyzer 🕵️‍♂️✨")
st.markdown("""
**AAKA AI API Key Analyzer** detecta automáticamente la plataforma de una clave API ingresada (OpenAI, DeepSeek, Anthropic) y proporciona un resumen de recursos disponibles como modelos, asistentes y almacenes vectoriales.
""")

# Input: API Key
api_key = st.text_input("Enter your API KEY", type="password")

# Detect Platform from API Key
def identify_platform(key):
    if key.startswith("sk-ant-"):
        headers = {"x-api-key": key}
        response = requests.get("https://api.anthropic.com/v1/models", headers=headers)
        return "Anthropic" if response.status_code == 200 else "Unknown or Invalid Anthropic Key"
    elif key.startswith("ds-"):
        headers = {"Authorization": f"Bearer {key}"}
        response = requests.get("https://api.deepseek.com/v1/models", headers=headers)
        return "DeepSeek" if response.status_code == 200 else "Unknown or Invalid DeepSeek Key"
    elif key.startswith("sk-"):
        openai.api_key = key
        try:
            openai.models.list()
            return "OpenAI"
        except Exception:
            return "Unknown or Invalid OpenAI Key"
    else:
        return "Unknown Platform"

# On Button Click
if st.button("Identify API Platform"):
    if not api_key:
        st.error("Please enter an API KEY.")
    else:
        with st.spinner("Querying the API platform..."):
            platform = identify_platform(api_key)
            st.success(f"✅ Platform Identified: **{platform}**")

            # ---- OPENAI ----
            if platform == "OpenAI":
                openai.api_key = api_key

                # Assistants
                try:
                    assistants = openai.beta.assistants.list().data
                    st.subheader("🤖 Assistants")
                    if assistants:
                        for assistant in assistants:
                            st.write(f"- {assistant.name} (ID: `{assistant.id}`)")
                    else:
                        st.info("No assistants found.")
                except Exception as e:
                    st.error("Failed to fetch assistants.")

                # Vector Stores
                try:
                    vector_stores = openai.vector_stores.list().data
                    st.subheader("🗂️ Vector Stores (RAGs)")
                    if vector_stores:
                        for store in vector_stores:
                            st.write(f"- {store.name} (ID: `{store.id}`)")
                    else:
                        st.info("No vector stores found.")
                except Exception as e:
                    st.error("Failed to fetch vector stores.")

                # Models (moved to end)
                try:
                    models = openai.models.list().data
                    st.subheader("📚 Available Models")
                    st.caption(f"Total Models: {len(models)}")
                    for model in models:
                        st.write(model.id)
                except Exception:
                    st.error("Failed to fetch models from OpenAI.")

            # ---- DEEPSEEK ----
            elif platform == "DeepSeek":
                headers = {"Authorization": f"Bearer {api_key}"}
                response = requests.get("https://api.deepseek.com/v1/models", headers=headers)
                if response.status_code == 200:
                    models = response.json().get("data", [])
                    st.subheader("📚 Available Models")
                    if models:
                        for model in models:
                            st.write(model.get("id"))
                    else:
                        st.info("No models found.")
                else:
                    st.error("Failed to fetch models from DeepSeek.")

            # ---- ANTHROPIC ----
            elif platform == "Anthropic":
                headers = {"x-api-key": api_key}
                response = requests.get("https://api.anthropic.com/v1/models", headers=headers)
                if response.status_code == 200:
                    models = response.json().get("data", [])
                    st.subheader("📚 Available Models")
                    if models:
                        for model in models:
                            st.write(model.get("id"))
                    else:
                        st.info("No models found.")
                else:
                    st.error("Failed to fetch models from Anthropic.")

            else:
                st.warning("⚠️ Unable to fetch additional details for this platform.")

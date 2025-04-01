import streamlit as st
import openai
import requests

# App Title and Description
st.title("🔑 AAKA AI API Key Analyzer 🕵️‍♂️✨")
st.markdown("""
**AAKA (AI API Key Analyzer)** detecta automáticamente la plataforma asociada con una clave API (OpenAI, DeepSeek, Anthropic) y muestra información sobre los modelos, asistentes y vector stores disponibles.
""")

# Input: API Key
api_key = st.text_input("🔐 Ingresa tu API KEY", type="password")

# Plataforma
def identify_platform(key):
    # Intentar primero con OpenAI
    if key.startswith("sk-") or key.startswith("pk-"):
        openai.api_key = key
        try:
            openai.models.list()
            return "OpenAI"
        except Exception:
            # Si no funciona como OpenAI, intentamos DeepSeek
            headers = {"Authorization": f"Bearer {key}"}
            try:
                response = requests.get("https://api.deepseek.com/openai/v1/models", headers=headers)
                if response.status_code == 200:
                    return "DeepSeek"
            except Exception:
                pass
            return "Unknown or Invalid Key"
    
    elif key.startswith("sk-ant-"):
        headers = {"x-api-key": key}
        response = requests.get("https://api.anthropic.com/v1/models", headers=headers)
        return "Anthropic" if response.status_code == 200 else "Unknown or Invalid Anthropic Key"
    
    else:
        return "Unknown Platform"

# On Button Click
if st.button("🔍 Identificar Plataforma de API"):
    if not api_key:
        st.error("Por favor ingresa una API Key.")
    else:
        with st.spinner("Consultando plataforma..."):
            platform = identify_platform(api_key)
            st.success(f"✅ Plataforma Detectada: **{platform}**")

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
                        st.info("No se encontraron asistentes.")
                except Exception:
                    st.error("No se pudo obtener la lista de assistants.")

                # Vector Stores
                try:
                    vector_stores = openai.vector_stores.list().data
                    st.subheader("🗂️ Vector Stores (RAGs)")
                    if vector_stores:
                        for store in vector_stores:
                            st.write(f"- {store.name} (ID: `{store.id}`)")
                    else:
                        st.info("No se encontraron vector stores.")
                except Exception:
                    st.error("No se pudo obtener la lista de vector stores.")

                # Models
                try:
                    models = openai.models.list().data
                    st.subheader("📚 Modelos Disponibles")
                    st.caption(f"Total de modelos: {len(models)}")
                    for model in models:
                        st.write(model.id)
                except Exception:
                    st.error("No se pudo obtener la lista de modelos.")

            # ---- DEEPSEEK ----
            elif platform == "DeepSeek":
                headers = {"Authorization": f"Bearer {api_key}"}
                response = requests.get("https://api.deepseek.com/openai/v1/models", headers=headers)
                if response.status_code == 200:
                    models = response.json().get("data", [])
                    st.subheader("📚 Modelos Disponibles")
                    if models:
                        for model in models:
                            st.write(model.get("id"))
                    else:
                        st.info("No se encontraron modelos.")
                else:
                    st.error(f"No se pudo obtener la lista de modelos de DeepSeek.")
                    st.code(response.text)

            # ---- ANTHROPIC ----
            elif platform == "Anthropic":
                headers = {"x-api-key": api_key}
                response = requests.get("https://api.anthropic.com/v1/models", headers=headers)
                if response.status_code == 200:
                    models = response.json().get("data", [])
                    st.subheader("📚 Modelos Disponibles")
                    if models:
                        for model in models:
                            st.write(model.get("id"))
                    else:
                        st.info("No se encontraron modelos.")
                else:
                    st.error("No se pudo obtener la lista de modelos de Anthropic.")

            else:
                st.warning("⚠️ No fue posible obtener detalles adicionales para esta plataforma.")

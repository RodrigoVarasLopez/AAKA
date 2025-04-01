import streamlit as st
import requests
from openai import OpenAI

# App Title and Description
st.title("🔑 AAKA AI API Key Analyzer 🕵️‍♂️✨")
st.markdown("""
**AAKA (AI API Key Analyzer)** detecta automáticamente la plataforma asociada con una clave API (OpenAI, DeepSeek, Anthropic) y muestra información sobre los modelos, asistentes y vector stores disponibles.
""")

# Input: API Key
api_key = st.text_input("🔐 Ingresa tu API KEY", type="password")


# Plataforma
def identify_platform(key):
    if key.startswith("sk-") or key.startswith("pk-"):
        try:
            client = OpenAI(api_key=key)
            client.models.list()
            return "OpenAI"
        except:
            try:
                client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
                client.models.list()
                return "DeepSeek"
            except:
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
                client = OpenAI(api_key=api_key)

                # Assistants
                try:
                    assistants = client.beta.assistants.list().data
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
                    vector_stores = client.vector_stores.list().data
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
                    models = client.models.list().data
                    st.subheader("📚 Modelos Disponibles")
                    st.caption(f"Total de modelos: {len(models)}")
                    for model in models:
                        st.write(model.id)
                except Exception:
                    st.error("No se pudo obtener la lista de modelos.")

            # ---- DEEPSEEK ----
            elif platform == "DeepSeek":
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                try:
                    models = client.models.list().data
                    st.subheader("📚 Modelos Disponibles (DeepSeek)")
                    if models:
                        for model in models:
                            st.write(f"- {model.id}")
                    else:
                        st.info("No se encontraron modelos.")
                except Exception as e:
                    st.error("Error al obtener modelos de DeepSeek.")
                    st.code(str(e))

            # ---- ANTHROPIC ----
            elif platform == "Anthropic":
                headers = {"x-api-key": api_key}
                response = requests.get("https://api.anthropic.com/v1/models", headers=headers)
                if response.status_code == 200:
                    models = response.json().get("data", [])
                    st.subheader("📚 Modelos Disponibles (Anthropic)")
                    if models:
                        for model in models:
                            st.write(f"- {model.get('id')}")
                    else:
                        st.info("No se encontraron modelos.")
                else:
                    st.error("No se pudo obtener la lista de modelos de Anthropic.")

            else:
                st.warning("⚠️ No fue posible obtener detalles adicionales para esta plataforma.")

import streamlit as st
import requests
import logging
from openai import OpenAI
import anthropic

# App title and description
st.title("🔑 AAKA AI API Key Analyzer 🕵️‍♂️✨")
st.markdown("""
**AAKA (AI API Key Analyzer)** automatically detects the platform associated with an API key (OpenAI, DeepSeek, Anthropic) and displays available models, assistants, and vector stores.
""")

# Input for API key
api_key = st.text_input("🔐 Enter your API KEY", type="password")

# Preview the entered key format
if api_key:
    st.caption(f"🔍 Key format preview: `{api_key[:8]}...{api_key[-4:]}`")

# Validate Anthropic key using Claude 3 Haiku
def is_valid_anthropic_key(api_key: str) -> tuple[bool, str]:
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[
                {"role": "user", "content": "What is artificial intelligence?"}
            ]
        )
        return True, "OK"
    except Exception as e:
        return False, str(e)

# Detect platform
def identify_platform(key):
    # First check for Anthropic
    if key.startswith("sk-ant-"):
        valid, error = is_valid_anthropic_key(key)
        if valid:
            return "Anthropic"
        else:
            logging.warning(f"Anthropic key validation error: {error}")
            st.error("❌ Anthropic key validation failed: Invalid or unauthorized API key.")
            return "Unknown or Invalid Anthropic Key"

    # Then try OpenAI and DeepSeek
    elif key.startswith("sk-") or key.startswith("pk-"):
        try:
            client = OpenAI(api_key=key)
            client.models.list()
            return "OpenAI"
        except Exception as e_openai:
            try:
                client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
                client.models.list()
                return "DeepSeek"
            except Exception as e_deepseek:
                st.error("❌ Failed with OpenAI and DeepSeek.")
                return "Unknown or Invalid Key"

    else:
        st.error("❌ Unknown key format. Could not match OpenAI, DeepSeek, or Anthropic.")
        return "Unknown Platform"

# When button is clicked
if st.button("🔍 Identify API Platform"):
    if not api_key:
        st.error("Please enter an API key.")
    else:
        with st.spinner("Detecting platform..."):
            platform = identify_platform(api_key)
            st.success(f"✅ Platform Detected: **{platform}**")

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
                        st.info("No assistants found.")
                except Exception:
                    st.error("Failed to fetch assistants.")

                # Vector Stores
                try:
                    vector_stores = client.vector_stores.list().data
                    st.subheader("🗂️ Vector Stores (RAGs)")
                    if vector_stores:
                        for store in vector_stores:
                            st.write(f"- {store.name} (ID: `{store.id}`)")
                    else:
                        st.info("No vector stores found.")
                except Exception:
                    st.error("Failed to fetch vector stores.")

                # Models
                try:
                    models = client.models.list().data
                    st.subheader("📚 Available Models")
                    st.caption(f"Total models: {len(models)}")
                    for model in models:
                        st.write(model.id)
                except Exception:
                    st.error("Failed to fetch models.")

            # ---- DEEPSEEK ----
            elif platform == "DeepSeek":
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                try:
                    models = client.models.list().data
                    st.subheader("📚 Available Models (DeepSeek)")
                    if models:
                        for model in models:
                            st.write(f"- {model.id}")
                    else:
                        st.info("No models found.")
                except Exception as e:
                    st.error("Failed to fetch models from DeepSeek.")
                    st.code(str(e))

            # ---- ANTHROPIC ----
            elif platform == "Anthropic":
                try:
                    st.subheader("📚 Commonly Available Models (Anthropic)")
                    st.markdown("""
                    Anthropic does not allow listing models via API.  
                    These are some commonly available models:
                    """)
                    models = [
                        "claude-3-haiku-20240307",
                        "claude-3-sonnet-20240229",
                        "claude-3-opus-20240229"
                    ]
                    for model in models:
                        st.write(f"- {model}")
                except Exception as e:
                    st.error("Could not process Anthropic key.")
                    st.code(str(e))

            # ---- UNKNOWN ----
            else:
                st.warning("⚠️ Could not retrieve additional information for this platform.")

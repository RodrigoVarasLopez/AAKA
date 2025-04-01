import streamlit as st
import requests
from openai import OpenAI
import anthropic

# App title and description
st.title("🔑 AAKA AI API Key Analyzer 🕵️‍♂️✨")
st.markdown("""
**AAKA (AI API Key Analyzer)** automatically detects the platform associated with an API key (OpenAI, DeepSeek, Anthropic) and displays available models, assistants, and vector stores.
""")

# Input for API key
api_key = st.text_input("🔐 Enter your API KEY", type="password")


# Validate Anthropic API key using Claude 3 Haiku (most accessible model)
def is_valid_anthropic_key(api_key: str) -> tuple[bool, str]:
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-haiku-20240307",  # the most universally available Claude 3 model
            max_tokens=10,
            messages=[
                {"role": "user", "content": "What is artificial intelligence?"}
            ]
        )
        return True, "OK"
    except Exception as e:
        return False, str(e)


# Identify the platform based on the API key
def identify_platform(key):
    if key.startswith("sk-") or key.startswith("pk-"):
        # Try OpenAI
        try:
            client = OpenAI(api_key=key)
            client.models.list()
            return "OpenAI"
        except:
            # If not OpenAI, try DeepSeek with custom base URL
            try:
                client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
                client.models.list()
                return "DeepSeek"
            except:
                return "Unknown or Invalid Key"

    elif key.startswith("sk-ant-"):
        valid, error = is_valid_anthropic_key(key)
        if valid:
            return "Anthropic"
        else:
            st.error("❌ Anthropic key validation failed:")
            st.code(error)
            return "Unknown or Invalid Anthropic Key"

    else:
        return "Unknown Platform"


# Trigger platform detection when button is clicked
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

                # List Assistants
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

                # List Vector Stores
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

                # List Models
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
                    Anthropic doesn't support listing models via API.  
                    However, the following are commonly available:
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

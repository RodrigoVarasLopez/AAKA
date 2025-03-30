import streamlit as st
import openai
import requests

st.title("🔑 AAKA 🕵️‍♂️✨")

# Input API Key
api_key = st.text_input("Enter your API KEY", type="password")

# Function to identify the platform
def identify_platform(key):
    if key.startswith("sk-ant-"):
        # Test Anthropic API
        headers = {"x-api-key": key}
        response = requests.get("https://api.anthropic.com/v1/models", headers=headers)
        if response.status_code == 200:
            return "Anthropic"
        else:
            return "Unknown or Invalid Anthropic Key"
    elif key.startswith("ds-"):
        # Test DeepSeek API
        headers = {"Authorization": f"Bearer {key}"}
        response = requests.get("https://api.deepseek.com/v1/models", headers=headers)
        if response.status_code == 200:
            return "DeepSeek"
        else:
            return "Unknown or Invalid DeepSeek Key"
    elif key.startswith("sk-"):
        # Test OpenAI API
        openai.api_key = key
        try:
            openai.models.list()
            return "OpenAI"
        except:
            return "Unknown or Invalid OpenAI Key"
    else:
        return "Unknown Platform"

# Button to identify API
if st.button("Identify API Platform"):
    if not api_key:
        st.error("Please enter an API KEY.")
    else:
        platform = identify_platform(api_key)
        st.write(f"Identified Platform: **{platform}**")

        # If OpenAI, list resources
        if platform == "OpenAI":
            models = openai.models.list().data
            st.subheader("Available Models")
            for model in models:
                st.write(model.id)

            # List Assistants
            assistants = openai.beta.assistants.list().data
            st.subheader("Assistants")
            if assistants:
                for assistant in assistants:
                    st.write(f"- {assistant.name} (ID: {assistant.id})")
            else:
                st.write("No Assistants found.")

            # List Vector Stores
            vector_stores = openai.vector_stores.list().data
            st.subheader("Vector Stores (RAGs)")
            if vector_stores:
                for store in vector_stores:
                    st.write(f"- {store.name} (ID: {store.id})")
            else:
                st.write("No Vector Stores found.")

        elif platform == "DeepSeek":
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://api.deepseek.com/v1/models", headers=headers)
            if response.status_code == 200:
                models = response.json().get("data", [])
                st.subheader("Available Models")
                for model in models:
                    st.write(model.get("id"))
            else:
                st.error("Failed to fetch models from DeepSeek.")

        elif platform == "Anthropic":
            headers = {"x-api-key": api_key}
            response = requests.get("https://api.anthropic.com/v1/models", headers=headers)
            if response.status_code == 200:
                models = response.json().get("data", [])
                st.subheader("Available Models")
                for model in models:
                    st.write(model.get("id"))
            else:
                st.error("Failed to fetch models from Anthropic.")
        else:
            st.warning("Unable to fetch additional details for this platform.")

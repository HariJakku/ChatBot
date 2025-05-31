import streamlit as st
from ibm_watsonx_ai.foundation_models import ModelInference

# IBM Watsonx Credentials
api_key = "ImbPt-KTxJT6tR_dJVbpDO6Ey6VcLyVkG-Fnuh2iafTE"
project_id = "fe0cbd91-220b-4ada-bed0-966bda1e316e"
base_url = "https://eu-de.ml.cloud.ibm.com"
model_id = "ibm/granite-13b-instruct-v2"

# System prompt to guide the assistant’s behavior
system_prompt = """
You are an intelligent assistant that provides accurate, helpful, and factual answers
about technology, computer science, current world facts, and definitions.

Example:
User: What is ML?
Assistant: Machine Learning (ML) is a subfield of artificial intelligence focused on algorithms that learn from data.

User: What is DSA?
Assistant: DSA stands for Data Structures and Algorithms, which are fundamental concepts in computer science.

Now, answer the following question:
"""

# Streamlit UI
st.set_page_config(page_title="Watsonx ChatBot", page_icon="🤖")
st.title("🤖 Watsonx ChatBot")
st.caption(f"Model: {model_id}")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for i in range(0, len(st.session_state.chat_history), 2):
    with st.chat_message("user"):
        st.write(st.session_state.chat_history[i])
    if i + 1 < len(st.session_state.chat_history):
        with st.chat_message("assistant"):
            st.write(st.session_state.chat_history[i + 1])

# User input
user_input = st.chat_input("Type your message here...")

# On user input
if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.chat_history.append(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Initialize the Watsonx model using ModelInference
                model = ModelInference(
                    model_id=model_id,
                    credentials={
                        "apikey": api_key,  # Note: 'apikey' not 'api_key'
                        "url": base_url
                    },
                    project_id=project_id
                )

                # Build prompt with system instruction + user query
                final_prompt = f"{system_prompt}\nUser: {user_input}\nAssistant:"

                # Generate response
                response = model.generate_text(
                    prompt=final_prompt,
                    params={
                        "max_new_tokens": 500,
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "decode_method": "sample",
                        "stop_sequences": ["<|endoftext|>", "User", "Assistant"]
                    }
                )

                # Safe response handling
                if isinstance(response, dict) and "generated_text" in response:
                    bot_response = response["generated_text"].strip()
                else:
                    bot_response = str(response).strip()

                # Fallback response
                if not bot_response:
                    bot_response = "I'm not sure about that. Could you please rephrase your question?"

                st.write(bot_response)
                st.session_state.chat_history.append(bot_response)

            except Exception as e:
                st.error(f"❌ Error occurred while generating response:\n\n{e}")
                st.info("Please verify your credentials and check your internet connection.")

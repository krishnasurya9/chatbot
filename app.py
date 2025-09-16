import os
import sys
import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate

# --- API Key setup ---
sys.path.append(r"A:\projects\safe")
from KEYS import google_Key
os.environ["GOOGLE_API_KEY"] = google_Key

# --- Model Setup ---
model = init_chat_model(
    "gemini-1.5-flash-latest",
    model_provider="google_genai",
    temperature=0.7
)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=model, memory=memory, verbose=True)

# --- Prompt Template (Jack Sparrow style) ---
prompt_template = ChatPromptTemplate.from_template(
    "You are Captain Jack Sparrow. Answer every question with wit and iconic dialogues. Question: {question}"
)

# --- Streamlit UI ---
st.set_page_config(page_title="Jack Sparrow Chatbot", page_icon="🏴‍☠️")
st.title("☠️ Captain Jack Sparrow Chatbot")

# Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask something, matey..."):
    # Show user input
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Format prompt and get response
    formatted_prompt = prompt_template.format_messages(question=prompt)
    response = conversation.predict(input=formatted_prompt[0].content)

    # Show bot response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate

# --- Load API Key from Streamlit secrets ---
google_key = os.getenv("GOOGLE_API_KEY")
if not google_key:
    st.error("❌ GOOGLE_API_KEY not found! Please set it in Streamlit Secrets.")
    st.stop()  # Stop execution if no key

# --- Initialize model with API key (force usage) ---
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    google_api_key=google_key
)

# --- Conversation memory ---
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=model, memory=memory, verbose=True)

# --- Prompt template ---
prompt_template = ChatPromptTemplate.from_template(
    "You are Captain Jack Sparrow. Answer every question with wit and iconic dialogues. Question: {question}"
)

# --- Streamlit UI ---
st.set_page_config(page_title="Jack Sparrow Chatbot", page_icon="🏴‍☠️")
st.title("☠️ Captain Jack Sparrow Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask something, matey..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Format prompt and get response
    formatted_prompt = prompt_template.format_messages(question=prompt)
    response = conversation.predict(input=formatted_prompt[0].content)

    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

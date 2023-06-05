import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

models =  ["gpt-3.5-turbo", "gpt-4"]
MODEL = "gpt-3.5-turbo"



if 'messages' not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a helpful assistant."),
    ]

def get_result(temp, mess):
    chat = ChatOpenAI(temperature=temp,callbacks=[StreamingStdOutCallbackHandler()], model_name=MODEL)
    st.session_state.messages.append(HumanMessage(content=mess))
    response = chat(st.session_state.messages)
    st.session_state.messages.append(response)
    return response.content



st.title("Chatbot")


if st.session_state.messages:
    for i,m in enumerate(st.session_state.messages):
        message(m.content, is_user = i%2)


with st.form("my_form"):
    MODEL = st.selectbox("Model", models)
    temp = st.slider("Set the temperature",0.0,1.0, step=0.05)
    message = st.text_input("Your message")
    submitted = st.form_submit_button("Submit")
    if submitted:
       st.write(get_result(temp,message))
       st.experimental_rerun()

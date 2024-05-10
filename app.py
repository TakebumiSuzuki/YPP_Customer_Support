__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import conversation_logic as logic
import constants as K

st.set_page_config(
     page_title = K.TAB_PAGE_TITLE,
     page_icon = K.TAB_PAGE_ICON,
     layout = "wide",
     initial_sidebar_state = "expanded"
)

st.markdown("""
    <style>
        header {visibility: hidden;}
        div[class^='block-container'] { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True
)

st.title(K.TITLE)
st.write(K.WRITE)
print(st.session_state)
if "store" not in st.session_state:
    st.session_state["store"] = {}
message_list = logic.get_messages(st.session_state["store"])

# Display chat messages from history on app rerun
if message_list != []:
    for message in message_list:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    clear_history = st.button("会話履歴を消去")
    if clear_history == True:
        st.session_state["store"] = {}
        st.session_state['retrived_text'] = ""
        clear_history = False
        st.rerun()

# Accept user input
if prompt := st.chat_input(K.HOLDER):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state['retrived_text'] = logic.invoke(prompt, st.session_state["store"])
    st.rerun()

with st.sidebar:
    st.write(K.SIDEBAR_WRITE)
    with st.container():
        if 'retrived_text' in st.session_state:
            st.markdown(st.session_state['retrived_text'])



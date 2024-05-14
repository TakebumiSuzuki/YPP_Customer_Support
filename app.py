# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import constants as K
import streamlit as st
import conversation_logic as logic

ss = st.session_state

st.set_page_config(
     page_title = K.TAB_PAGE_TITLE,
     page_icon = K.TAB_PAGE_ICON,
     layout = "wide",
     initial_sidebar_state = "expanded"
)

st.markdown("""
    <style>
        header {visibility: hidden;}
        div[class^='block-container'] { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True
)

st.title(K.TITLE)
st.write(K.WRITE)
if "store" not in ss:
    ss["store"] = []
message_list = ss["store"]

# Display chat messages from history on app rerun
if message_list != []:
    for message in message_list:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if "show_button" in ss and ss["show_button"] == True:
        clear_history = st.button("会話履歴を消去")
        if clear_history == True:
            ss["store"] = []
            ss['retrived_text'] = ""
            clear_history = False
            st.rerun()

def delete_button():
    ss["show_button"] = False

# Accept user input
if prompt := st.chat_input(K.HOLDER, on_submit=delete_button):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    ss['retrived_text'] = logic.invoke(prompt, ss["store"], ss["mode"])
    ss["show_button"] = True
    st.rerun()

with st.sidebar:
    if "mode" not in ss:
        ss["mode"] = "sim"
    selected_mode = st.radio(label = "Choose model", options = ["sim", "mmr"], horizontal = True)
    ss["mode"] = selected_mode
    if 'retrived_text' in ss:
        st.markdown(ss['retrived_text'])



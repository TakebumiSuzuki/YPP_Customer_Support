# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import constants as K
import streamlit as st
import conversation_logic as logic

ss = st.session_state
if "lang" not in ss:
    ss["lang"] = "日本語"
    st.write("ifnai desu")
lang = ss["lang"]

if "store" not in ss:
    ss["store"] = []
message_list = ss["store"]

# st.set_page_config(
#      page_title = K.TAB_TITLE(lang),
#      page_icon = K.TAB_ICON,
#      layout = "wide",
#      initial_sidebar_state = "expanded"
# )

st.markdown(K.CSS, unsafe_allow_html=True)

st.title(K.TITLE(lang))
st.write(K.SUBTITLE(lang))

# Display chat messages from history on app rerun
if message_list != []:
    for message in message_list:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # if message["role"] == "AI":
            #     st.button('docs履歴')

    if "show_button" in ss and ss["show_button"] == True:
        clear_button = st.button(K.CLEAR_BUTTON(lang))
        if clear_button == True:
            ss["store"] = []
            ss["retrived_text"] = ""
            clear_button = False
            st.rerun()

def delete_button():
    ss["show_button"] = False

# Accept user input
if input := st.chat_input(K.INPUT_HOLDER(lang), on_submit = delete_button):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(input)
    ss["retrived_text"] = logic.invoke(input, ss["store"], ss["lang"])
    ss["show_button"] = True
    st.rerun()

#Streamlitのおかしな仕様で、この中でselected_lang変数を使うことができるが、変更前の状態になっているため、
#これを使わず、冗長性はないがss["lang"]であべこべに選択肢体裁を保っている。一応動く
def set_language():
    if ss["lang"] == '日本語':
        ss["lang"] = 'EN'
    else:
        ss["lang"] = '日本語'
    print(ss["lang"])

st.write(("EN", "日本語").index(st.session_state["lang"]))
with st.sidebar:
    selected_lang = st.radio(label = "Choose language", options = ["EN", "日本語"], horizontal = True, index=("EN", "日本語").index(st.session_state["lang"]), on_change = set_language)

    if "retrived_text" in ss:
        st.markdown(ss["retrived_text"])




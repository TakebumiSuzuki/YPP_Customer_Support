import constants as K
import os
from dotenv import load_dotenv

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()
llm = ChatOpenAI(
    model= K.LLM_MODEL_NAME,
    temperature= K.LLM_TEMPERATURE,
    api_key=os.getenv(K.LLM_API_KEY)
    )

embeddings_model = OpenAIEmbeddings(
    model = K.EMBEDDING_MODEL_NAME,
    api_key = os.getenv(K.EMBEDDING_API_KEY)
    )

vectorstore = Chroma(
    persist_directory = K.VECSTORE_DIR,
    embedding_function = embeddings_model
    )

retriever = vectorstore.as_retriever(
        search_type = K.SEARCH_TYPE,
        search_kwargs={'k': K.K, 'fetch_k': K.FETCH_K}
)

### Contextualize question ###
contextualize_q_system_prompt = K.CONTEXTURIZE_PROMPT

contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")]
)

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

### Answer question ###
qa_system_prompt = K.QA_PROMPT

qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)


rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# ### Statefully manage chat history ###
# store = {}

def invoke(inputText, store):

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    response = conversational_rag_chain.invoke(
        {"input": inputText},
        config={"configurable": {"session_id": "abc123"}},  # constructs a key "abc123" in `store`.
    )
    documents = response['context']

    textData = ""
    for document in documents:
        text = document.page_content
        textData += '\n----------------------\n' + text
    return textData

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
def get_messages(store):
    if  'abc123' in store:
        messages = store['abc123'].messages
        message_list = []
        for message in messages:
            if type(message) is HumanMessage:
                text = message.content
                message_list.append({'role' : 'AI', 'content' : text} )
            if type(message) is AIMessage:
                text = message.content
                message_list.append({'role' : 'You', 'content' : text} )
    else:
        message_list = []

    return message_list

def clear_conversation():
    store == {}










# apiResponse = conversational_rag_chain.invoke(
#     {"input": "recommended speed needed to play the video?"},
#     config={
#         "configurable": {"session_id": "abc123"}
#     },  # constructs a key "abc123" in `store`.
# )

# print(apiResponse["answer"])
# print(store)


# InMemoryChatMessageHistory(
#     messages=[
#         HumanMessage(content='recommended speed needed to play the video?'),
#         AIMessage(content='The recommended sustained speeds needed to play videos on YouTube are as follows: 4K resolution requires 20 Mbps, HD 1080p requires 5 Mbps, HD 720p requires 2.5 Mbps, SD 480p requires 1.1 Mbps, and SD 360p requires 0.7 Mbps. You can check the resolution of the video you are trying to play and compare it to these recommended speeds to troubleshoot any playback issues.')
#         ]
# )





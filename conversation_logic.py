import constants as K
import os
from dotenv import load_dotenv
from uuid import uuid4
load_dotenv()

unique_id = uuid4().hex[0:8]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"Tracing Walkthrough - {unique_id}"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv(K.LANGSMITH_API_KEY)
from langsmith import Client
client = Client()

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings



from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere.rerank import CohereRerank
import cohere


compressor = CohereRerank(
    client = cohere.Client(os.getenv(K.COHERE_API_KEY)),
    top_n = 7,
    model = "rerank-multilingual-v3.0",
    cohere_api_key = os.getenv(K.COHERE_API_KEY)
)

from langchain_openai import OpenAI
llm = OpenAI(model_name="gpt-3.5-turbo-instruct")
# llm = ChatOpenAI(
#     model= K.LLM_MODEL_NAME,
#     temperature= K.LLM_TEMPERATURE,
#     api_key=os.getenv(K.LLM_API_KEY)
#     )

embeddings_model = OpenAIEmbeddings(
    model = K.EMBEDDING_MODEL_NAME,
    api_key = os.getenv(K.EMBEDDING_API_KEY)
    )

vectorstore = Chroma(
    persist_directory = K.VECSTORE_DIR,
    embedding_function = embeddings_model
    )

from langchain_core.runnables import ConfigurableField
retriever = vectorstore.as_retriever(
        search_type = "similarity_score_threshold",
        search_kwargs = {'k': K.K, 'score_threshold': K.THRESH},
        )
# .configurable_alternatives(
#             ConfigurableField(id = 'retriever'),
#             default_key = "sim",
#             # This adds a new option, with name `openai` that is equal to `ChatOpenAI()`
#             mmr = Chroma(
#                 persist_directory = K.VECSTORE_DIR,
#                 embedding_function = embeddings_model
#                 ).as_retriever(
#                     search_type = "mmr",
#                     search_kwargs={'k': K.K, 'fetch_k': K.FETCH_K}
#                     )
# )



compression_retriever = ContextualCompressionRetriever(
    base_compressor = compressor,
    base_retriever = retriever,
)




### Contextualize question ###
contextualize_q_system_prompt = K.CONTEXTURIZE_PROMPT

contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
        ])

# ***********************************
# history_aware_retriever = create_history_aware_retriever(
#     llm, retriever, contextualize_q_prompt
# )
history_aware_retriever = create_history_aware_retriever(
    llm, compression_retriever, contextualize_q_prompt
)
# ***********************************

### Answer question ###
qa_system_prompt = K.QA_PROMPT

qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)


rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


def invoke(inputText, store, mode):

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

    response = conversational_rag_chain.with_config(configurable={"retriever": mode}).invoke(
        {"input": inputText},
        config={"configurable": {"session_id": "abc123"}},  # constructs a key "abc123" in `store`.
    )
    print(response['chat_history'])
    documents = response['context']

    textData = ""
    for document in documents:
        text = document.page_content
        textData += text + '\n---\n'
    return textData

# from langchain_core.chat_history import InMemoryChatMessageHistory
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
        if len(messages) > K.CHAT_HIST_NUM:
            messages = messages[:K.CHAT_HIST_NUM]
    else:
        message_list = []

    return message_list




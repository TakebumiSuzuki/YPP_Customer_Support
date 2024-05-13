import constants as K
import os
from dotenv import load_dotenv
from uuid import uuid4
load_dotenv()



from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import cohere

co = cohere.Client(os.getenv(K.COHERE_API_KEY))

embeddings_model = OpenAIEmbeddings(
    model = K.EMBEDDING_MODEL_NAME,
    api_key = os.getenv(K.EMBEDDING_API_KEY)
    )

vectorstore = Chroma(
    persist_directory = K.VECSTORE_DIR,
    embedding_function = embeddings_model
    )

retriever = vectorstore.as_retriever(
        search_type = "similarity_score_threshold",
        search_kwargs = {'k': K.K, 'score_threshold': K.THRESH},
        )

def invoke(inputText, store, mode):
    response = co.chat(
        model = "command-r-plus",
        preamble = K.HYDE_PROMPT,
        temperature = 0.3,
        message = inputText,
    )
    query = response.text
    print(query)

    docs = retriever.invoke(query)
    for i in range(len(docs)):
        print(docs[i].page_content)
        print("\n-------------\n")

    docs = docs[:4]
    qa_system_prompt = K.QA_PROMPT

    qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system_prompt),
            ("human", "{input}")]
    )
    from langchain_google_genai import GoogleGenerativeAI
    llm = GoogleGenerativeAI(model="models/gemini-1.5-pro-latest", google_api_key=os.getenv(K.GEMINI_API_KEY))

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    answer = question_answer_chain.invoke({"input": inputText, "context": docs})
    print("----answer is-------")
    print(answer)
    store.append({"role" : "user", "content" : inputText})
    store.append({"role" : "AI", "content" : answer})

    source_text = ""
    for doc in docs:
        text = doc.page_content
        source_text += text + '\n---\n'
    return source_text



# from langchain_core.chat_history import InMemoryChatMessageHistory
# from langchain_core.messages.human import HumanMessage
# from langchain_core.messages.ai import AIMessage
# def get_messages(store):
#     if  'abc123' in store:
#         messages = store['abc123'].messages
#         message_list = []
#         for message in messages:
#             if type(message) is HumanMessage:
#                 text = message.content
#                 message_list.append({'role' : 'AI', 'content' : text} )
#             if type(message) is AIMessage:
#                 text = message.content
#                 message_list.append({'role' : 'You', 'content' : text} )
#         if len(messages) > K.CHAT_HIST_NUM:
#             messages = messages[:K.CHAT_HIST_NUM]
#     else:
#         message_list = []

#     return message_list




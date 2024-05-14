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

co = cohere.Client(
    os.getenv(K.COHERE_API_KEY)
)

embeddings_model = OpenAIEmbeddings(
    model = K.EMBEDDING_MODEL_NAME,
    api_key = os.getenv(K.OPENAI_API_KEY)
    )

from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model=K.GEMINI_MODEL_NAME, google_api_key=os.getenv(K.GEMINI_API_KEY))


def invoke(inputText, store, lang):
    language = (
        "English" if lang == "EN" else
        "Japanese"
        )

    response = co.chat(
        model = K.COHERE_MODEL_NAME,
        preamble = K.HYDE_PROMPT.format(language, language),
        temperature = 0.3,
        message = inputText,
    )

    query = response.text
    print("\n-------------\n")
    print(query)
    print("\n-------------\n")

    vectorstore = Chroma(
        persist_directory = (
            K.EN_VECSTORE if lang == "EN" else
            K.JA_VECSTORE
        ),
        embedding_function = embeddings_model
    )

    retriever = vectorstore.as_retriever(
        search_type = K.SEARCH_TYPE,
        search_kwargs = {'k': K.K, 'score_threshold': K.THRESH},
    )

    docs = retriever.invoke(query)
    for i in range(len(docs)):
        # print(docs[i].page_content)
        print("\n-------------\n")

    docs = docs[:4]
    qa_system_prompt = K.QA_PROMPT

    qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system_prompt),
            ("user", "{input}")]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    answer = question_answer_chain.invoke({"input": inputText, "context": docs, "language": language})
    print("----answer is-------")
    print(answer)
    store.append({"role" : "user", "content" : inputText})
    store.append({"role" : "AI", "content" : answer})

    source_text = ""
    for doc in docs:
        text = doc.page_content
        source_text += text + '\n---\n'
    return source_text




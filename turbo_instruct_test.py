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

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings



input = "イエローアイコンはそのままにしていても良いの？"
import cohere

co = cohere.Client(os.getenv(K.COHERE_API_KEY))
response = co.chat(
    model = "command-r-plus",
    preamble = K.CONTEXTURIZE_PROMPT,
    temperature = 0.3,
    message = input,
    )
query = response.text
print(query)

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

docs = retriever.invoke(query)
text_docs = []
for i in range(len(docs)):
    print(docs[i].page_content)
    print("\n-------------\n")
    if i < 4:
        text_docs.append(docs[i].page_content)

docs = docs[:4]

qa_system_prompt = K.QA_PROMPT

qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        ("human", "{input}")]
)
from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model="models/gemini-1.5-pro-latest", google_api_key=os.getenv(K.GEMINI_API_KEY))

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
res = question_answer_chain.invoke({"input": input, "context": docs})
print(res)



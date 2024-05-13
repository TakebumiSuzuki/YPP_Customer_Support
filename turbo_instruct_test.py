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




# from langchain_openai import OpenAI

# llm = OpenAI(model_name="gpt-3.5-turbo-instruct")
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

from langchain_core.runnables import ConfigurableField
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
# print(
#     llm.invoke(
#         "What are some of the pros and cons of Python as a programming language?"
#     )
# )

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
res = question_answer_chain.invoke({"input": input, "context": docs})
print(res)



# print(response2.text)

# # contextualize_q_system_prompt = K.CONTEXTURIZE_PROMPT
# # contextualize_q_prompt = ChatPromptTemplate.from_messages([
# #         ("system", contextualize_q_system_prompt),
# #         ("human", "{input}")
# #         ])

# # from langchain.retrievers.multi_query import MultiQueryRetriever
# # retriever_from_llm = MultiQueryRetriever.from_llm(
# #     retriever=vectorstore.as_retriever(), llm=llm
# # )

# # from langchain.chains import create_history_aware_retriever, create_retrieval_chain

# # result = history_aware_retriever = create_history_aware_retriever(
# #     llm, retriever_from_llm, contextualize_q_prompt
# #     )


# from langchain_core.prompts.prompt import PromptTemplate
# from langchain.retrievers.re_phraser import RePhraseQueryRetriever
# re_phrase_retriever = RePhraseQueryRetriever.from_llm(
#     retriever = retriever,
#     llm = llm,
#     prompt = PromptTemplate.from_template(K.CONTEXTURIZE_PROMPT)
# )

# # import cohere


# # compressor = CohereRerank(
# #     client = cohere.Client(os.getenv(K.COHERE_API_KEY)),
# #     top_n = 7,
# #     model = "rerank-multilingual-v3.0",
# #     cohere_api_key = os.getenv(K.COHERE_API_KEY)
# # )

# # compression_retriever = ContextualCompressionRetriever(
# #     base_compressor = compressor,
# #     base_retriever = re_phrase_retriever,
# # )

# print(re_phrase_retriever.invoke("再利用コンテンツと認定されてしまいました、そんなつもりはないのですが、どうしたら良いでしょうか"))



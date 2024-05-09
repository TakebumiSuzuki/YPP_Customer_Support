TAB_PAGE_TITLE = 'AIサポセン'
TAB_PAGE_ICON = None
TITLE = 'Partner Manager AI サポート'
WRITE = '会話メモリー: メッセージ過去6回分のみ記憶してます'
HOLDER = 'YouTubeに関する質問のみ'
SIDEBAR_WRITE = '以下、情報元です'

LLM_MODEL_NAME = 'gpt-3.5-turbo'
LLM_TEMPERATURE = 0.4
LLM_API_KEY = 'OPENAI_API_KEY'
EMBEDDING_API_KEY = 'OPENAI_API_KEY'
EMBEDDING_MODEL_NAME = 'text-embedding-3-large'
VECSTORE_DIR = 'data_en.chroma_db'
SEARCH_TYPE = 'mmr'
K = 4
FETCH_K = 15

CONTEXTURIZE_PROMPT = """Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."""

QA_PROMPT = """You are a support agent working at YouTube customer support. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

{context}"""



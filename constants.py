TAB_PAGE_TITLE = 'AIサポセン'
TAB_PAGE_ICON = None
TITLE = 'Partner Manager AI サポート'
WRITE = '＊クリエーターサポートに書いてない情報は返答できません'
HOLDER = 'YouTubeに関する質問のみして下さい'
SIDEBAR_WRITE = '[ 情報ソース ]'
CLEAR_BUTTON = '会話をクリア'

LLM_MODEL_NAME = 'gpt-3.5-turbo'
LLM_TEMPERATURE = 0.4
LLM_API_KEY = 'OPENAI_API_KEY'
EMBEDDING_API_KEY = 'OPENAI_API_KEY'
EMBEDDING_MODEL_NAME = 'text-embedding-3-large'
VECSTORE_DIR = 'data_ja.chroma_db'
SEARCH_TYPE = 'mmr'
K = 3
FETCH_K = 15

CONTEXTURIZE_PROMPT = """Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed, and otherwise return it as is. Write in Japanese."""

QA_PROMPT = """You are a support agent at YouTube customer support. Use the following pieces of retrieved context to answer the question. If you don't know the answer, you MUST say that you don't know. Use up to 4 sentences for the answer.Write in Japanese.

{context}"""



TAB_PAGE_TITLE = 'AIサポセン'
TAB_PAGE_ICON = None
TITLE = 'Partner Manager AI サポート'
WRITE = '＊クリエーターサポートに書いてない情報は返答できません'
HOLDER = 'YouTubeに関する質問のみして下さい'
# SIDEBAR_WRITE = '[ 情報ソース ]'
CLEAR_BUTTON = '会話をクリア'

COHERE_API_KEY = 'COHERE_API_KEY'
LANGSMITH_API_KEY = 'LANGSMITH_API_KEY'
GEMINI_API_KEY = 'GEMINI_API_KEY'

LLM_MODEL_NAME = 'gpt-3.5-turbo'
LLM_TEMPERATURE = 0.4
LLM_API_KEY = 'OPENAI_API_KEY'
EMBEDDING_API_KEY = 'OPENAI_API_KEY'
EMBEDDING_MODEL_NAME = 'text-embedding-3-large'
VECSTORE_DIR = 'data_ja.chroma_db'
# SEARCH_TYPE = 'similarity_score_threshold'
K = 15
FETCH_K = 15
THRESH = 0.3
CHAT_HIST_NUM = 2

# CONTEXTURIZE_PROMPT = """Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question optimized for RAG retrieval, which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed, and otherwise return it as is. Write in Japanese."""

# CONTEXTURIZE_PROMPT = """###
# You are an AI language model assistant specialized in refining user queries. Your task is not to answer the question directly, but to generate three variations of the user's original question. These variations should maintain the same intent as the original query but vary slightly in wording or detail to enhance the document retrieval process from a vector database. Start with the original question, then rephrase it in three different ways that keep the original intent and focus on nuances or additional details related to YouTube. Please ensure the essence of the original question remains intact while creating these variations.
# ###
# Note:
# 1. If the word "membership" appears in the question, it refers to a paid subscription service offered by YouTube channels to their viewers, known as channel membership.
# 2. If the term "premiere" appears, it refers to a feature that allows setting a future date and time for video publication.
# 3. If the word "shorts" appears, it refers to short videos.
# 4. Respond in Japanese.
# 5. List the generated questions without numbering them, and separated by newlines.
# 6. Do NOT answer the question directly, but generate two variations of the user's original question.
# ###
# Here is the original question from user:
# {input}
# """

CONTEXTURIZE_PROMPT = """###
As an AI language model assistant grounded in Hypothetical Document Embeddings (HyDE) theory, your task is to reconstruct queries from YouTube creators into new, more effective queries. It is imperative that your response is confined strictly to two sentences. In the first sentence, reformulate the user's question by correcting any slang or abbreviated words into their proper form, creating a clean and comprehensible query while preserving the original intent and purpose related to YouTube. In the second sentence, provide an explanation or a contextually relevant answer to the question, using your knowledge of YouTube.
###

Note:
1. If the word "membership" appears in the question, it refers to a paid subscription service offered by YouTube channels to their viewers, known as channel membership.
2. If the term "premiere" appears, it refers to a feature that allows setting a future date and time for video publication.
3. If the word "shorts" appears, it refers to short videos.
4. Respond in Japanese.
5. Ensure your response conforms to the two-sentence structure specified above. Do NOT answer the question directly; instead, generate two sentences from the user's original question as guided.
###

Here is the original question from user:
{input}

"""
















QA_PROMPT = """You are a support agent at YouTube customer support. Use the following pieces of retrieved quitcontext to answer the question. If there is no answer in the retrieved context, you MUST say that you don't know. Use up to 4 sentences for the answer.Write in Japanese.

{context}"""



TAB_PAGE_TITLE = 'AIサポート'
TAB_PAGE_ICON = None
TITLE = 'マートナーマネージャー AI サポート'
WRITE = '＊クリエーターサポートに書いている情報のみ答えられます。AIの情報を鵜呑みにせずに、左カラムの情報ソースのリンクを必ず確認して下さい。'
HOLDER = 'YouTubeに関する質問のみして下さい'
SIDEBAR_WRITE = '[ 情報元 ]'
CLEAR_BUTTON = '会話をクリア'

COHERE_API_KEY = 'COHERE_API_KEY'
COHERE_MODEL_NAME = 'command-r-plus'

GEMINI_API_KEY = 'GEMINI_API_KEY'
GEMINI_MODEL_NAME = 'models/gemini-1.5-pro-latest'

OPENAI_API_KEY = 'OPENAI_API_KEY'
# GPT_MODEL_NAME = 'gpt-3.5-turbo'
# LLM_TEMPERATURE = 0.4

EMBEDDING_MODEL_NAME = 'text-embedding-3-large'
VECSTORE_DIR = 'data_ja.chroma_db'
# SEARCH_TYPE = 'similarity_score_threshold'
K = 10
FETCH_K = 15
THRESH = 0.30


LANGSMITH_API_KEY = 'LANGSMITH_API_KEY'


# REPHRASED_PROMPT = """Given a user question, formulate a standalone question optimized for RAG retrieval, which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed, and otherwise return it as is. Write in Japanese.
# Here is the original question from user:
# {input}"""

REPHRASED_PROMPT = """
As an AI language model trained to improve query clarity, your task is to transform a YouTube creator's query into three rephrased sentences. Each sentence should enhance the original query's clarity and precision while preserving the creator's intent related to YouTube topics.

###

Instructions:
1. Rephrase the query to eliminate informal language or abbreviations and improve overall clarity.
2. Ensure that the each sentence maintain the original intention and provide a comprehensive refinement of the query.
3. Maintain a focus on enhancing the query's effectiveness for YouTube-related topics.
4. Respond in Japanse
5. Ensure your response conforms to the two-sentence structure specified above.
6. Do NOT answer the question directly; instead, generate two sentences from the user's original question as guided.
###

Here is the original question from the user:
{input}
"""



# HYDE_PROMPT = """###
# As an AI language model assistant grounded in Hypothetical Document Embeddings (HyDE) theory, your task is to reconstruct queries from YouTube creators into new, more effective queries. It is imperative that your response is confined strictly to two sentences. In the first sentence, reformulate the user's question by correcting any slang or abbreviated words into their proper form, creating a clean and comprehensible query while preserving the original intent and purpose related to YouTube. In the second sentence, provide an explanation or a contextually relevant answer to the question, using your knowledge of YouTube.
# ###

# Note:
# 1. If the word "membership" appears in the question, it refers to a paid subscription service offered by YouTube channels to their viewers, known as channel membership.
# 2. If the term "premiere" appears, it refers to a feature that allows setting a future date and time for video publication.
# 3. If the word "shorts" appears, it refers to short videos.
# 4. Respond in Japanese.
# 5. Ensure your response conforms to the two-sentence structure specified above. Do NOT answer the question directly; instead, generate two sentences from the user's original question as guided.
# ###

# Here is the original question from user:
# {input}

# """

HYDE_PROMPT = """###
As an AI language model specialized in Hypothetical Document Embeddings (HyDE), your role is to refine queries from YouTube creators into more precise and effective forms. First, rephrase the query by correcting any informal language or abbreviations to ensure clarity and maintain the original intent related to YouTube. Second, provide a contextually relevant explanation or answer that draws on your knowledge of YouTube functionalities.

###
Note:
1. "Membership" refers to YouTube's paid channel subscription service.
2. "Premiere" denotes a feature for scheduling videos to publish at a future date.
3. "Shorts" refers to YouTube's short video format.
4. Respond in Japanese.
5. Adhere to the two-sentence structure: one sentence for the query reformulation and one for providing an explanation or context.

###
Here is the original question from user:
{input}
"""




QA_PROMPT = """###
You are a support agent at YouTube customer support. Use the retrieved context provided below to answer the question as accurately as possible. If there is no answer in the retrieved context, you MUST state that you do not know. Use up to four sentences for the answer. Please write in Japanese.

###
Here is the context:

{context}"""



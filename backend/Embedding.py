#processing the given file 
#steps
#   1.chunking 
#   2.embedding
#   3.storing (vector spaces/store) chromaDB...
#_____________________________________#


from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_community.vectorstores import Chroma

# from langchain.retrievers import ContextualCompressionRetriever
# from langchain.retrievers.document_compressors import EmbeddingsFilter



def load_and_chunk(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    chunks = splitter.split_documents(docs)
    return chunks


def add_to_vectorstore(chunk):
    embeddings = MistralAIEmbeddings(
        model="mistral-embed",
    )
    vectorstore = Chroma(
            embedding_function=embeddings,
            persist_directory="./chroma_db",
            collection_name="all_documents"
        )   
    vectorstore.add_documents(chunk)
    vectorstore.persist()
    # return vectorstore

def query_vectorstore(query_text):
    embeddings = MistralAIEmbeddings(model="mistral-embed")

    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory="./chroma_db",
        collection_name="all_documents"
    )
    base_retriver = vectorstore.as_retriever(search_type="similarity_score_threshold",search_kwargs={"k": 6,"score_threshold": 0.5})
    # base_retriver = vectorstore.as_retriever(
    #         search_type="mmr",
    #         search_kwargs={
    #             "k": 6,
    #             "fetch_k": 25,       # candidates to choose from
    #             "lambda_mult": 0.8   # 0.0=diversity, 1.0=relevance
    #         }
    #     )
    llm = ChatMistralAI(model="mistral-large-latest")

    retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriver,
        llm=llm
    )
    
    results = retriever.invoke(query_text)
    if not results:
        return{
            "status":"No match",
            "message":"No relevent information found in the uploaded documents.",
            "results":[]
        }
    return {
        "status":"ok",
        "results":results
    }


async def process_doc(file_path):
    chunks = load_and_chunk(file_path)
    add_to_vectorstore(chunks)
    return {"status": "document indexed"}
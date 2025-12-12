#processing the given file 
#steps
#	1.chunking 
#	2.embedding
#	3.storing (vector spaces/store) chromaDB...
#_____________________________________#


from dotenv import load_dotenv
load_dotenv()


from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_mistralai import ChatMistralAI
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader

def chunking(doc):

	text_splitter=RecursiveCharacterTextSplitter(
		chunk_size=1000,
		chunk_overlap=200,
		add_start_index=True
		)
	chunks = text_splitter.split_documents(docs)
	return chunks



# def embedding(chunks):
#     embeddings = MistralAIEmbeddings(
#         model="mistral-embed",
#     )
#     # vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
#     vectorstore = InMemoryVectorStore.from_documents(
#         documents=chunks,
#         embedding=embeddings,
#     )

    # retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    # results = retriever.invoke("What is this gpt4v?")
    # print(results[0].page_content[:] + "...")



def Retrival_query(qurey,chunk):
	embeddings = MistralAIEmbeddings(
        model="mistral-embed",
    )
	vectorstore = Chroma.from_documents(
	        documents=chunk,
	        embedding=embeddings,
	        persist_directory="./chroma_db",
	        collection_name="all_documents"
	    )	
	llm = ChatMistralAI(model="mistral-large-latest")

	multi_retriever = MultiQueryRetriever.from_llm(
	    retriever=vectorstore.as_retriever(search_kwargs={"k": 6}),
	    llm=llm
	)

	# Single call → generates 3-5 query variants → retrieves from MULTIPLE docs
	results = multi_retriever.invoke(qurey)
	return results



# def multi_query_retrival(query):#--->wont work 
# 	llm = ChatMistralAI(model="mistral-large-latest")

# 	retriever = MultiQueryRetriever.from_llm(
# 		retriever=vectorstore.as_retriever(search_kwargs={"k": 6}),
#     	llm=llm,)

# 	results = retriever.invoke(query)
# 	# return results

# 	print("Top results covering all angles:")
# 	for i, doc in enumerate(results[:3], 1):
# 		print(f"\n{i}. {doc.page_content[:300]}...")



loader = DirectoryLoader("C:/Users/Sachi/Desktop/poject/forest/processor_tmp", glob="**/*.*",loader_cls=PyPDFLoader,show_progress=True)  # All PDFs in folder
docs = loader.load()
chunk=chunking(docs)


print(f"Loaded {len(docs)} docs → {len(chunk)} chunks")
print(type(chunk))


# multi_query_retrival("what is gpt4v ?") #cant use this


# embedding(chunk)
all_results = []
qu="Variants of GAN ?,What is a GAN ?"
results=Retrival_query(qu,chunk)
all_results.extend(results)
unique_results = {}
for doc in all_results:
    key = (doc.metadata['source'], hash(doc.page_content[:100]))
    unique_results[key] = doc



print("Results from ALL documents:")
for i, doc in enumerate(unique_results.values(), 1):
    print(f"\n{i}. {getattr(doc, 'page_content', str(doc))[:300]}...")



async def process_doc(file_path):
	return {"hi":"something"}


# async def process_doc(filepath: str):
#     """This is a process fucntion where we will send the data to furture processing 
#     	first step is chunking provided doc into smaller parts
#     ""



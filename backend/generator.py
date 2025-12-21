from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from Embedding import query_vectorstore
from pydantic import BaseModel
from typing import List
from pathlib import Path

class Slide(BaseModel):
    heading: str
    points: List[str]

class PPTResponse(BaseModel):
    title: str
    slides: List[Slide]

def generator_response(query_text: str):
    retrieval_response = query_vectorstore(query_text)

    if retrieval_response["status"] == "No match":
        return {
            "status": "No match",
            "message": "No relevant information found",
            "ppt": None
        }

    docs = retrieval_response["results"]
    context = "\n\n".join([doc.page_content for doc in docs])

    parser = JsonOutputParser(pydantic_object=PPTResponse)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are an expert teaching assistant.

Use ONLY the provided context.
Return VALID JSON only.
No markdown. No explanation.
"""),
        ("human", "{format_instructions}\n\nContext:\n{context}\n\nQuestion: {question}")
    ])

    llm = ChatMistralAI(model="mistral-large-latest")
    chain = prompt | llm | parser   # 🔑 IMPORTANT

    ppt = chain.invoke({
        "context": context,
        "question": query_text,
        "format_instructions": parser.get_format_instructions()
    })
    seen = set()
    sources = []

    for doc in docs:
        name = Path(doc.metadata.get("source", "")).name
        if name not in seen:
            seen.add(name)
            sources.append({"filename": name})

    return {
    "status": "ok",
    "ppt": ppt,
    "sources": sources
    }

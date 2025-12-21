from fastapi import FastAPI,File,UploadFile,BackgroundTasks,Request,Form
from pydantic import BaseModel
import pathlib, shutil, uuid
from Embedding import process_doc
from generator import generator_response
from fastapi.responses import HTMLResponse


from fastapi.staticfiles import StaticFiles
from doc_registry import load_registry, save_registry
import hashlib

from fastapi.staticfiles import StaticFiles

app=FastAPI()


# Serve frontend
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")

DOC_DIR=pathlib.Path("C:/Users/Sachi/Desktop/poject/forest/processor_tmp")
DOC_DIR.mkdir(exist_ok=True)

def compute_hash(file: UploadFile):
    h = hashlib.sha256()
    file.file.seek(0)
    h.update(file.file.read())
    file.file.seek(0)
    return h.hexdigest()

def render_html(ppt_json):
    html = f"<h1>{ppt_json['title']}</h1>"

    for slide in ppt_json["slides"]:
        html += f"<h2>{slide['heading']}</h2><ul>"
        for point in slide["points"]:
            html += f"<li>{point}</li>"
        html += "</ul>"

    return html


@app.get("/")
def earth():
    return {"function_name":"earth","using_fast_api":"RAG"}


@app.post("/upload_and_query")
async def upload_and_query(
    file: UploadFile | None = File(None),
    query: str = Form(...)
):
    # stored_path = DOC_DIR / file.filename
    # with stored_path.open("wb") as out:
    #     shutil.copyfileobj(file.file, out)
    # await process_doc(stored_path)

    registry = load_registry()

    if file:
        stored_path = DOC_DIR / file.filename

        with stored_path.open("wb") as out:
            shutil.copyfileobj(file.file, out)

        # compute hash FROM DISK (SAFE)
        file_hash = hashlib.sha256(stored_path.read_bytes()).hexdigest()

        hashed_path = DOC_DIR / f"{file_hash}_{file.filename}"

        # rename if new
        if not hashed_path.exists():
            stored_path.rename(hashed_path)
            await process_doc(hashed_path)   # ✅ ONLY here
        else:
            stored_path.unlink()             # already indexed, do nothing


        registry[file_hash] = {
            "filename": file.filename,
            "path": str(hashed_path),
            "indexed": True
        }
        save_registry(registry)
    response = generator_response(query)

    return {
        "query": query,
        "documents_indexed": len(registry),
        **response
    }

@app.post("/render/html")
async def render_html_view(payload: dict):
    ppt = payload.get("ppt")

    if not ppt:
        return HTMLResponse(
            content="<h2>No presentation data found</h2>",
            status_code=400
        )

    html = render_html(ppt)
    return HTMLResponse(content=html)



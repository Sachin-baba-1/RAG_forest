from fastapi import FastAPI,File,UploadFile,BackgroundTasks
from pydantic import BaseModel
import pathlib, shutil, uuid
from Embedding import process_doc


app=FastAPI()

@app.get("/")
def earth():
	return {"function_name":"earth","using_fast_api":"RAG"}



DOC_DIR=pathlib.Path("C:/Users/Sachi/Desktop/poject/forest/processor_tmp")
DOC_DIR.mkdir(exist_ok=True)

JOB_STATUS = {}

def mark_job_status(job_id: str, status: str):
	JOB_STATUS[job_id] = status

async def _run_and_record(file_path: str, job_id: str):
    try:
        mark_job_status(job_id, "processing")
        result = await process_doc(file_path)
        mark_job_status(job_id, "done:" + str(result))
    except Exception as e:
        mark_job_status(job_id, "failed:" + str(e))

@app.post("/input_HERE")
async def ocean(background: BackgroundTasks, Filee: UploadFile = File(...)):
    stored_name = Filee.filename
    stored_path = DOC_DIR / stored_name
    if stored_path.exists():
        return {"status": "skipped", "reason": "already exist"}

    with stored_path.open("wb") as f:
        shutil.copyfileobj(Filee.file, f)

    job_id = uuid.uuid4().hex
    mark_job_status(job_id, "queued")
    background.add_task(_run_and_record, str(stored_path), job_id)

    return {"status": "uploaded", "filename": stored_name, "job_id": job_id}

# @app.get("/status/{job_id}")
# def status(job_id: str):
#     return {"job_id": job_id, "status": JOB_STATUS.get(job_id, "not_found")}
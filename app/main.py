import shutil
import tempfile
import asyncio
import os
from xml.parsers.expat import errors
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.tools import analyze_errors_with_llm
from .agent import Agent
from pathlib import Path
from .log_tools import extract_errors, save_to_json

app = FastAPI()
agent = Agent()

# ----------  run_task summary ----------
class TaskRequest(BaseModel):
    input: str

@app.post("/summary_task/")
def run_task(task: TaskRequest):
    return agent.run_task(task.dict())

# ----------  upload portal  ----------

UPLOAD_DIR = Path("./upload_logs")
os.makedirs(UPLOAD_DIR, exist_ok=True)
temp_dir = tempfile.gettempdir()

async def process_log_file(file_path: str, output_json: str): 
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, process_log_file_sync, file_path, output_json)
    

def process_log_file_sync(file_path: str, output_json: str):
    errors = extract_errors(file_path)
    save_to_json(errors, output_json)
    return errors

@app.post("/upload_log/")
async def upload_log(top_n: int = 3, file: UploadFile = File(...)):
    """
    Upload a WildFly .log file, extract all ERROR-level log entries, 
    count their occurrences, and return the Top N most frequent errors.
    

    For each of these Top N errors, the service performs an LLM-based diagnostic analysis and returns the results in a structured JSON response.
    """
    if not file.filename.endswith(".log"):
        raise HTTPException(status_code=400, detail="Only .log files are allowed.")

    # use tempary file  
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, file.filename)

        with open(temp_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        try:
            errors_json = extract_errors(temp_file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing log file: {e}")

        # Use LLM to anaylize Top N errors
        try:
            analysis = analyze_errors_with_llm(errors_json, top_n)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error analyzing errors: {e}")

        # Summary of the analysis
        return JSONResponse(
            content={
                "filename": file.filename,
                "message": f"Below are the error analyses for the Top {top_n} most frequent errors.",
                "error_analysis": analysis
            }
        )


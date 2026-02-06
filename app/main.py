import shutil
import tempfile
import asyncio
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .agent import Agent
from pathlib import Path
from .log_tools import extract_errors, save_to_json

app = FastAPI()
agent = Agent()

# ---------- 原 run_task summary 接口 ----------
class TaskRequest(BaseModel):
#    检查请求数据合法性（input） + 生成文档。
    input: str

@app.post("/run_task/")
def run_task(task: TaskRequest):
    return agent.run_task(task.dict())

# ---------- 新增 portal 上传接口 ----------

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
# 异步调用，不会堵塞API
async def upload_log(file: UploadFile = File(...)):
    if not file.filename.endswith(".log"):
        raise HTTPException(status_code=400, detail="Only .log files are allowed.")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # temp_dir = tempfile.gettempdir()   返回的是系统全局临时目录（比如 /tmp 或 C:\Users\Vina\AppData\Local\Temp），不能直接删除整个目录，会把系统的全局临时文件都删掉，非常危险。
        temp_file_path = os.path.join(temp_dir, file.filename)
        output_json = os.path.join(temp_dir, file.filename + "_errors.json")

        with open(temp_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # 解析日志文件，提取错误信息
        try:
            errors = await process_log_file(temp_file_path, output_json)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing log file: {e}")
        
        return JSONResponse(content={"filename": file.filename, "errors": errors})
    #     return JSONResponse(
    #     content={
    #         "message": f"Log processed, {len(log_data)} error/warn/failed entries saved.",
    #         "json_file": output_json
    #     }
    # )

    


    # 1. buffer 和 f 的区别是什么？
    # 2. shutil 做什么的？
from fastapi import FastAPI, HTTPException
from tasks import *
import os

app = FastAPI()


@app.post("/run")
async def run_task(task: str):
    try:
        if "format" in task and ".md" in task:
            format_markdown("/data/format.md")
            return {"status": "success"}

        elif "count Wednesdays" in task:
            count_wednesdays("/data/dates.txt", "/data/dates-wednesdays.txt")
            return {"status": "success"}

        elif "convert markdown" in task:
            convert_md_to_html("/data/docs/input.md", "/data/docs/output.html")
            return {"status": "success"}

        elif "run SQL" in task:
            run_sql_query("/data/ticket-sales.db", "/data/ticket-sales-gold.txt")
            return {"status": "success"}

        else:
            raise HTTPException(status_code=400, detail="Unsupported task")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_file(path: str):
    enforce_security(path)

    try:
        with open(path, "r") as file:
            return {"content": file.read()}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

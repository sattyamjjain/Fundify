from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from store.handler import (
    upload_statements,
    initiate_statement_analysis,
    Statement,
    get_analyzed_statement,
)
from utils import get_logger

app = FastAPI()

logger = get_logger()


@app.post("/api/upload-statement/")
async def upload_statement(bank_name: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        error_message = "Invalid file type. Only .csv files are accepted."
        logger.error(f"Upload Failed: {error_message}")
        raise HTTPException(status_code=400, detail=error_message)
    try:
        statement_id = await upload_statements(
            _file=file, bank_name=bank_name, file_name=file.filename
        )
        logger.info(f"Statement uploaded successfully: {statement_id}")
        return {"statement_id": statement_id}
    except FileExistsError as e:
        logger.error(f"Upload Failed - FileExistsError: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Upload Failed - Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/initiate-analyze/")
async def initiate_analyze(statement: Statement):
    try:
        await initiate_statement_analysis(statement.statement_id)
        return {"message": "Initiated Statement Analyzer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analyzed-statement/{statement_id}")
async def get_analyzed_statements(statement_id: str):
    try:
        analyzed_statement = await get_analyzed_statement(statement_id)
        return {"statement": analyzed_statement}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

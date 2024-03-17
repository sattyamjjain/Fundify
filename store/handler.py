import os

import pandas as pd
from fastapi import UploadFile
from pydantic import BaseModel

from config import STORE_CONFIG
from store.publisher.publisher import MQTTPublisher
from store.service import read_statements_file, upload_statement_file


class Statement(BaseModel):
    statement_id: str


async def upload_statements(_file: UploadFile, bank_name: str, file_name: str) -> str:
    return await upload_statement_file(_file, bank_name, file_name)


async def initiate_statement_analysis(statement_id: str, chunk_size: int = 10):
    _statements_df = await read_statements_file(statement_id)
    unique_transactions = _statements_df["Narration"].unique()
    MQTTPublisher().initiate_statement_analyzer(
        statement_id=statement_id,
        unique_transactions=unique_transactions,
        chunk_size=chunk_size,
    )


async def get_analyzed_statement(statement_id: str):
    analyze_statements_file_path = os.path.join(
        STORE_CONFIG["analyzed_statements_folder_path"], f"{statement_id}.csv"
    )
    if not os.path.isfile(analyze_statements_file_path):
        raise FileNotFoundError(f"File not found for {statement_id}.csv")
    categorized_transaction_df = pd.read_csv(analyze_statements_file_path)
    return categorized_transaction_df.to_json()

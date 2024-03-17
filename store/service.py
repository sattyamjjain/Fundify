import hashlib
import os
from io import StringIO

import aiofiles
import pandas as pd
from fastapi import HTTPException, UploadFile

from config import STORE_CONFIG
from utils import get_logger, ensure_directory

logger = get_logger()


async def read_statements_file(statement_id: str) -> pd.DataFrame:
    file_path = os.path.join(
        STORE_CONFIG["statements_folder_path"], f"{statement_id}.csv"
    )

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Statement file not found.")

    async with aiofiles.open(file_path, mode="r") as file:
        content = await file.read()

    return pd.read_csv(StringIO(content))


def _get_statement_id(bank_name: str, file_name: str):
    hasher = hashlib.sha256()
    hasher.update(f"{bank_name}__{file_name.split('.')[0]}".encode())
    return hasher.hexdigest()


@ensure_directory("statements_folder_path")
async def upload_statement_file(_file: UploadFile, bank_name: str, file_name: str):
    _statement_id = _get_statement_id(bank_name, file_name)

    file_path = os.path.join(
        STORE_CONFIG["statements_folder_path"], f"{_statement_id}.csv"
    )

    if os.path.exists(file_path):
        raise FileExistsError(f"A file with the name {file_name} already exists.")

    async with aiofiles.open(file_path, "wb") as buffer:
        await buffer.write(await _file.read())

    return _statement_id

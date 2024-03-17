import os

import pandas as pd

from config import STORE_CONFIG
from utils import ensure_directory, save_dataframe


def clean_transaction(_transaction):
    parts = _transaction.split("'")
    return parts[1] if len(parts) == 3 else _transaction


def parse_transactions(_transactions: str) -> pd.DataFrame:
    transaction_category_pairs = [
        line.split("::") for line in _transactions.split("\n") if "::" in line
    ]
    transactions = [clean_transaction(t[0]) for t in transaction_category_pairs]
    categories = [t[1].strip() for t in transaction_category_pairs]
    return pd.DataFrame({"Transaction": transactions, "Category": categories})


@ensure_directory("categorize_transactions_folder_path")
def upload_categorized_transactions(statement_id: str, transactions_df: pd.DataFrame):
    file_path = os.path.join(
        STORE_CONFIG["categorize_transactions_folder_path"], f"{statement_id}.csv"
    )
    save_dataframe(
        transactions_df, file_path, append=True if os.path.isfile(file_path) else False
    )


@ensure_directory("analyzed_statements_folder_path")
def upload_analyzed_statements(statement_id: str):
    print(os.getcwd())

    statements_df = pd.read_csv(
        os.path.join(STORE_CONFIG["statements_folder_path"], f"{statement_id}.csv")
    )
    categorized_transaction_df = pd.read_csv(
        os.path.join(
            STORE_CONFIG["categorize_transactions_folder_path"], f"{statement_id}.csv"
        )
    )

    analyze_statements_df = pd.merge(
        statements_df,
        categorized_transaction_df,
        left_on="Narration",
        right_on="Transaction",
        how="left",
    )
    analyze_statements_df.drop("Transaction", axis=1, inplace=True)

    analyze_statements_file_path = os.path.join(
        STORE_CONFIG["analyzed_statements_folder_path"], f"{statement_id}.csv"
    )

    save_dataframe(
        analyze_statements_df,
        analyze_statements_file_path,
        append=True if os.path.isfile(analyze_statements_file_path) else False,
    )

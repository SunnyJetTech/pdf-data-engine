import pdfplumber
import pandas as pd
from typing import BinaryIO, Any
from fastapi import (Request, Depends, HTTPException, status)
from sqlalchemy.orm import Session
from db.database import get_db
from core.Models import User
from auth.jwt_handler import decode_token
from db.database import DBConnection

def extract_pdf_table(pdf_source: str | BinaryIO) -> pd.DataFrame:
    records: list[list[str]] = []
    max_cols = 0

    with pdfplumber.open(pdf_source) as pdf:
        total_pages = len(pdf.pages)

        for page_no, page in enumerate(pdf.pages, start=1):
            print(f"Processing page {page_no}/{total_pages}")
            tables = page.extract_tables()

            for table in tables:
                if not table:
                    continue

                for row in table:
                    clean_row = [str(cell).strip() if cell is not None else "" for cell in row]

                    max_cols = max(max_cols, len(clean_row))
                    records.append(clean_row)

    if not records:
        raise ValueError("No table data found in PDF.")

    for row in records:
        while len(row) < max_cols:
            row.append("")

    columns = [f"Column{i}" for i in range(1, max_cols + 1)]

    return pd.DataFrame(records, columns=columns)

def process_headers(df: pd.DataFrame, has_header: int):
    display_columns = {}

    if has_header not in (0, 1):
        raise ValueError("has_header must be 0 or 1")

    if has_header == 0:
        for col in df.columns:
            display_columns[col] = col
        return df, display_columns

    first_row = df.iloc[0]

    for idx, col in enumerate(df.columns):
        header_value = str(first_row.iloc[idx]).strip()

        if not header_value:
            header_value = col

        display_columns[col] = header_value

    df = df.iloc[1:].reset_index(drop=True)
    return df, display_columns

def save_to_excel(df: pd.DataFrame, excel_file: str):

    df.to_excel(excel_file, index=False)
    print(f"Saved Excel: {excel_file}")

def save_to_database(df: pd.DataFrame, session: Session, table_name: str):
    df.to_sql(table_name, session.bind, if_exists="replace", index=False)

def save_metadata(display_columns: dict, session: Session, table_name: str):
    metadata_df = pd.DataFrame([
        {
            "table_name": table_name,
            "column_name": key,
            "display_name": value
        }
        for key, value in display_columns.items()
    ])

    metadata_df.to_sql(
        "column_metadata",
        session.bind,
        if_exists="append",
        index=False
    )
    
def resolve_column(user_input: str, df: pd.DataFrame, display_columns: dict):
    user_input = user_input.strip()

    if user_input.isdigit():
        index = int(user_input) - 1
        if index < 0 or index >= len(df.columns):
            raise ValueError("Invalid column number")

        return df.columns[index]

    for col, display in display_columns.items():

        if display.lower() == user_input.lower():
            return col

    raise ValueError(f"Column '{user_input}' not found")


def apply_filter(df: pd.DataFrame, column: str, operator: str, value: str):

    series = df[column].astype(str)

    if operator == "=":
        return df[series.str.strip() == value]

    if operator == "!=":
        return df[series.str.strip() != value]

    if operator == "contains":
        return df[series.str.contains(value, case=False, na=False)]

    if operator == "startswith":
        return df[series.str.startswith(value, na=False)]

    if operator == "endswith":
        return df[series.str.endswith(value, na=False)]

    if operator in (">", "<", ">=", "<="):

        numeric = pd.to_numeric(series, errors="coerce")
        value = float(value)

        if operator == ">":
            return df[numeric > value]

        if operator == "<":
            return df[numeric < value]

        if operator == ">=":
            return df[numeric >= value]

        if operator == "<=":
            return df[numeric <= value]

    raise ValueError(f"Unsupported operator: {operator}")

def search_dataframe(df: pd.DataFrame, display_columns: dict, filters: list[dict]):
    result = df.copy()

    for item in filters:
        column = resolve_column(item["column"], result, display_columns)

        result = apply_filter(result, column, item["operator"], str(item["value"]))

    return result

def process_pdf(pdf_source: str | BinaryIO, has_header: int, save_excel: bool = False, save_db: bool = False,
    excel_file: str = "output.xlsx", table_name: str = "pdf_data", session: Session | None = None
):
    df = extract_pdf_table(pdf_source)
    df, display_columns = process_headers(df, has_header)

    if save_excel:
        save_to_excel(df, excel_file)

    if save_db and session:
        save_to_database(df, session, table_name)
        save_metadata(display_columns, session, table_name)

    return {
        "dataframe": df,
        "display_columns": display_columns,
        "row_count": len(df),
        "column_count": len(df.columns)
    }

def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authentication token")

    payload = decode_token(token)
    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


def get_optional_user(request: Request, db: Session = Depends(get_db)):
    try:
        return get_current_user_from_cookie(request, db)

    except HTTPException:
        return None
    
def user_required(current_user: User = Depends(get_current_user_from_cookie)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")

    return current_user

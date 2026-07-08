import pdfplumber
import pandas as pd
from typing import BinaryIO, Callable, Awaitable
from sqlalchemy.orm import Session
from core.utils.dataframe import process_headers, save_to_excel, save_metadata
from core.utils.mongodb import save_to_mongodb

MAX_PAGES = 1000
MAX_ROWS = 500000

async def extract_pdf_table(pdf_source: str | BinaryIO, has_header: bool = True, progress_callback: Callable[[int, int], Awaitable[None]] | None = None) -> pd.DataFrame:
    records: list[list[str]] = []
    headers: list[str] | None = None
    max_cols = 0

    with pdfplumber.open(pdf_source) as pdf:
        total_pages = len(pdf.pages)
        
        
        if total_pages > MAX_PAGES:
            raise ValueError(
                f"PDF exceeds maximum page limit ({MAX_PAGES})"
            )
            
        for page_no, page in enumerate(pdf.pages, start=1):

            print(f"Processing page {page_no}/{total_pages}")

            if progress_callback:
                await progress_callback(page_no, total_pages)

            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:
                if not table:
                    continue

                if has_header and headers is None:
                    header_row = table[0]

                    headers = [str(cell).strip() if cell is not None else f"Column{i + 1}" for i, cell in enumerate(header_row)]
                    max_cols = len(headers)
                    print(f"Detected headers: {headers}")

                    data_rows = table[1:]
                else:
                    data_rows = table

                for row in data_rows:
                    clean_row = [str(cell).strip() if cell is not None else "" for cell in row]

                    max_cols = max(max_cols, len(clean_row))
                    records.append(clean_row)

    if not records:
        raise ValueError("No table data found in PDF.")

    if len(records) > MAX_ROWS:
        raise ValueError(
            f"Dataset exceeds maximum row limit ({MAX_ROWS:,})"
        )

    for row in records:
        while len(row) < max_cols:
            row.append("")

    if headers:
        while len(headers) < max_cols:
            headers.append(f"Column{len(headers) + 1}")

        columns = headers

    else:
        columns = [f"Column{i}" for i in range(1, max_cols + 1)]

    return pd.DataFrame(records, columns=columns)

def process_pdf(pdf_source: str | BinaryIO, has_header: int, save_excel: bool = False, save_db: bool = False,
    excel_file: str = "output.xlsx", table_name: str = "pdf_data", session: Session | None = None
):
    df = extract_pdf_table(pdf_source)
    df, display_columns = process_headers(df, has_header)

    if save_excel:
        save_to_excel(df, excel_file)

    if save_db and session:
        save_to_mongodb(df, session, table_name)
        save_metadata(display_columns, session, table_name)

    return {
        "dataframe": df,
        "display_columns": display_columns,
        "row_count": len(df),
        "column_count": len(df.columns)
    }
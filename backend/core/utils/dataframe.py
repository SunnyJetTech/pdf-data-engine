import pandas as pd
from sqlalchemy.orm import Session

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
    
def save_to_excel(df: pd.DataFrame, excel_file: str):

    df.to_excel(excel_file, index=False)
    print(f"Saved Excel: {excel_file}")
    

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

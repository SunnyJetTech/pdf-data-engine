import pandas as pd
from db.mongo_db import mongodb

def save_to_mongodb(dataframe: pd.DataFrame, collection_name: str,):
    collection = mongodb[collection_name]

    collection.delete_many({})

    rows = (dataframe.fillna("").to_dict(orient="records"))

    if rows:
        collection.insert_many(rows)
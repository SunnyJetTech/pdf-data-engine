from __future__ import annotations
from typing import Callable
import pandas as pd
from core.constants.search import SearchOperator
from schemas.search.filter import SearchFilter
from schemas.search.query_result import QueryResult
from schemas.search.request import SearchRequest

class DatasetQueryService:

    _OPERATORS: dict[SearchOperator, Callable] = {}

    @classmethod
    def query(cls, dataframe: pd.DataFrame, request: SearchRequest) -> QueryResult:

        df = dataframe.copy()

        if request.filters:
            df = cls._apply_filters(df, request.filters)

        total = len(df)

        if request.sort:
            df = cls._apply_sort(df, request.sort)

        if request.columns:
            df = cls._select_columns(df, request.columns)

        df = cls._paginate(
            df,
            page=request.page,
            page_size=request.page_size,
        )

        return QueryResult(
            dataframe=df,
            total=total,
            page=request.page,
            page_size=request.page_size,
        )

    @classmethod
    def _apply_filters(cls, dataframe: pd.DataFrame, filters: list[SearchFilter]) -> pd.DataFrame:

        df = dataframe

        for search_filter in filters:

            handler = cls._operator_map().get(search_filter.operator)

            if handler is None:
                raise ValueError(f"Unsupported operator: {search_filter.operator}")

            df = handler(df, search_filter)

        return df

    @classmethod
    def _operator_map(cls):

        if cls._OPERATORS:
            return cls._OPERATORS

        cls._OPERATORS = {
            SearchOperator.EQ: cls._equal,
            SearchOperator.NE: cls._not_equal,
            SearchOperator.GT: cls._greater_than,
            SearchOperator.GTE: cls._greater_equal,
            SearchOperator.LT: cls._less_than,
            SearchOperator.LTE: cls._less_equal,
            SearchOperator.CONTAINS: cls._contains,
            SearchOperator.STARTSWITH: cls._startswith,
            SearchOperator.ENDSWITH: cls._endswith,
            SearchOperator.IN: cls._in,
            SearchOperator.NOT_IN: cls._not_in,
            SearchOperator.IS_NULL: cls._is_null,
            SearchOperator.IS_NOT_NULL: cls._is_not_null,
        }

        return cls._OPERATORS

    @staticmethod
    def _validate_column(dataframe: pd.DataFrame, column: str):

        if column not in dataframe.columns:
            raise ValueError(f"Column '{column}' does not exist.")
        
    @classmethod
    def _equal(cls, df, f):

        cls._validate_column(df, f.column)

        return df[df[f.column] == f.value]

    @classmethod
    def _not_equal(cls, df, f):

        cls._validate_column(df, f.column)

        return df[df[f.column] != f.value]
    
    @classmethod
    def _greater_than(cls, df, f):

        cls._validate_column(df, f.column)

        return df[pd.to_numeric( df[f.column], errors="coerce") > float(f.value)]

    @classmethod
    def _greater_equal(cls, df, f):

        cls._validate_column(df, f.column)

        return df[pd.to_numeric(df[f.column], errors="coerce") >= float(f.value)]

    @classmethod
    def _less_than(cls, df, f):

        cls._validate_column(df, f.column)

        return df[pd.to_numeric(df[f.column], errors="coerce",)<float(f.value)]

    @classmethod
    def _less_equal(cls, df, f):

        cls._validate_column(df, f.column)

        return df[pd.to_numeric(df[f.column], errors="coerce")<=float(f.value)]
    
    @classmethod
    def _contains(cls, df, f):

        cls._validate_column(df, f.column)

        return df[df[f.column].fillna("").astype(str).str.contains(str(f.value), case=False, na=False )]

    @classmethod
    def _startswith(cls, df, f):

        cls._validate_column(df, f.column)

        return df[df[f.column].fillna("").astype(str).str.startswith(str(f.value), na=False)]

    @classmethod
    def _endswith(cls, df, f):

        cls._validate_column(df, f.column)

        return df[df[f.column].fillna("").astype(str).str.endswith(str(f.value), na=False)]

    @classmethod
    def _in(cls, df, f):

        cls._validate_column(df, f.column)

        values = (f.value if isinstance(f.value, list) else [f.value])

        return df[df[f.column].isin(values)]

    @classmethod
    def _not_in(cls, df, f):

        cls._validate_column(df, f.column)

        values = (f.value if isinstance(f.value, list) else [f.value])

        return df[~df[f.column].isin(values)]

    @classmethod
    def _is_null(cls, df, f):

        cls._validate_column(df, f.column)

        return df[df[f.column].isna()]

    @classmethod
    def _is_not_null(cls, df, f):

        cls._validate_column(df, f.column)

        return df[df[f.column].notna()]

    @classmethod
    def _apply_sort(cls, dataframe: pd.DataFrame, sort) -> pd.DataFrame:

        cls._validate_column(dataframe, sort.column)

        ascending = (sort.direction.value.lower() == "asc")

        return dataframe.sort_values(by=sort.column, ascending=ascending, kind="stable")

    @classmethod
    def _select_columns(cls, dataframe: pd.DataFrame, columns: list[str]) -> pd.DataFrame:

        valid_columns = [column for column in columns if column in dataframe.columns]

        if not valid_columns:

            return dataframe

        return dataframe[valid_columns]

    @staticmethod
    def _paginate(dataframe: pd.DataFrame, *, page: int, page_size: int) -> pd.DataFrame:

        if page < 1:
            page = 1

        if page_size < 1:
            page_size = 50

        start = (
            page - 1
        ) * page_size

        end = start + page_size

        return dataframe.iloc[
            start:end
        ].reset_index(drop=True)
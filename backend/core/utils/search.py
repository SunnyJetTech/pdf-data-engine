import pandas as pd

def resolve_column(user_input: str, dataframe: pd.DataFrame, display_columns: dict,):
    user_input = user_input.strip()

    if user_input.isdigit():
        index = int(user_input) - 1

        if index >= len(dataframe.columns):
            raise ValueError("Invalid column")

        return dataframe.columns[index]

    for db_column, display in display_columns.items():

        if display.lower() == user_input.lower():
            return db_column

    raise ValueError(
        f"Column '{user_input}' not found"
    )


def apply_filter(dataframe: pd.DataFrame, column: str, operator: str, value: str,):

    series = dataframe[column].astype(str)

    match operator:

        case "=":
            return dataframe[
                series.str.strip() == value
            ]

        case "!=":
            return dataframe[
                series.str.strip() != value
            ]

        case "contains":
            return dataframe[
                series.str.contains(
                    value,
                    case=False,
                    na=False,
                )
            ]

        case "startswith":
            return dataframe[
                series.str.startswith(value)
            ]

        case "endswith":
            return dataframe[
                series.str.endswith(value)
            ]

        case ">" | "<" | ">=" | "<=":

            numeric = pd.to_numeric(
                series,
                errors="coerce",
            )

            value = float(value)

            if operator == ">":
                return dataframe[numeric > value]

            if operator == "<":
                return dataframe[numeric < value]

            if operator == ">=":
                return dataframe[numeric >= value]

            return dataframe[numeric <= value]

        case _:
            raise ValueError(
                "Unsupported operator"
            )


def search_dataframe(dataframe: pd.DataFrame, display_columns: dict, filters: list[dict],):

    result = dataframe.copy()

    for item in filters:

        column = resolve_column(
            item["column"],
            result,
            display_columns,
        )

        result = apply_filter(
            result,
            column,
            item["operator"],
            str(item["value"]),
        )

    return result
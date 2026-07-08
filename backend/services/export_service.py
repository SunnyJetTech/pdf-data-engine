from io import BytesIO, StringIO
import pandas as pd

class ExportService:
    @staticmethod
    def generate_csv(rows: list[dict]) -> StringIO:

        output = StringIO()

        if not rows:
            pd.DataFrame().to_csv(output, index=False)
            output.seek(0)
            return output

        df = pd.DataFrame(rows)

        df.to_csv(output, index=False)
        output.seek(0)

        return output

    @staticmethod
    def generate_excel(rows: list[dict]) -> BytesIO:

        output = BytesIO()

        if not rows:
            with pd.ExcelWriter(
                output,
                engine="openpyxl",
            ) as writer:
                pd.DataFrame().to_excel(
                    writer,
                    index=False,
                )

            output.seek(0)
            return output

        df = pd.DataFrame(rows)

        with pd.ExcelWriter(
            output,
            engine="openpyxl",
        ) as writer:
            df.to_excel(
                writer,
                index=False,
            )

        output.seek(0)

        return output
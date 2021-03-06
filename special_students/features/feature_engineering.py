from typing import List

import pandas as pd

from special_students.settings import settings


class Features:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = self.load_df()

    def load_df(self):
        return pd.read_csv(self.filepath)

    @staticmethod
    def string_standardization(df: pd.DataFrame) -> pd.DataFrame:
        def process_string(text):
            if pd.isna(text):
                return text
            return text.strip().upper()

        string_columns = df.select_dtypes(include=object)
        for column in string_columns:
            df[column] = df[column].apply(process_string)

        return df

    @staticmethod
    def columns_concat_and_explode(
        df: pd.DataFrame, columns: List[str]
    ) -> pd.DataFrame:
        df["temp_col"] = df[columns].values.tolist()
        df = (
            df.explode("temp_col")
            .rename(columns={"temp_col": "codigo_curso"})
            .dropna(subset=["codigo_curso"])
            .drop(columns=settings.courses_columns)
        )
        return df

    @staticmethod
    def count_disciplines(df: pd.DataFrame) -> pd.DataFrame:
        student_approvations = (
            df.groupby(by=["nome_aluno"])
            .count()
            .rename(columns={"codigo_curso": "disciplinas_aprovadas"})
        )

        df = df.merge(
            right=pd.DataFrame(student_approvations),
            on="nome_aluno",
            how="inner",
        )
        return df

    def generate(self):
        return (
            self.df.pipe(Features.string_standardization)
            .pipe(Features.columns_concat_and_explode, columns=settings.courses_columns)
            .pipe(Features.count_disciplines)
        )


def feature_engineering():
    features = Features(settings.interim_students_path)
    features.generate().to_csv(settings.interim_students_courses_path, index=False)


if __name__ == "__main__":
    feature_engineering()

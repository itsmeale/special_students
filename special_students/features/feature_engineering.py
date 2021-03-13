from typing import List

import pandas as pd

DISCIPLINES_COLUMNS: List[str] = ["disciplina_1", "disciplina_2", "disciplina_3"]


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
            .drop(columns=DISCIPLINES_COLUMNS)
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
            .pipe(Features.columns_concat_and_explode, columns=DISCIPLINES_COLUMNS)
            .pipe(Features.count_disciplines)
        )


if __name__ == "__main__":
    filepath = "data/interim/alunos.csv"
    features = Features(filepath)
    features.generate().to_csv("data/interim/alunos_cursos.csv", index=False)

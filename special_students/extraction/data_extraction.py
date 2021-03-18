from typing import List

import pandas as pd
import tabula


class MissingParameterException(Exception):
    pass


class Extraction:
    __filepath: str = None

    def __init__(self, filepath):
        self.__filepath = filepath

    def extract(self):
        dfs = self.__read_pdf()
        extracted_data = Extraction.__preprocess_dfs(dfs)
        return extracted_data

    def __read_pdf(self):
        if not self.__filepath:
            raise MissingParameterException("Filepath not defined yet")
        return tabula.io.read_pdf(
            self.__filepath, pages="all", pandas_options={"header": None}
        )

    @staticmethod
    def __preprocess_first_df(df: pd.DataFrame) -> pd.DataFrame:
        df = df.iloc[3:, :].rename(columns={1: "disciplinas"})
        df[[1, 2, 3]] = df["disciplinas"].str.split(" ", expand=True)
        return df.drop(columns=["disciplinas"])

    @staticmethod
    def __preprocess_dfs(dfs: List[pd.DataFrame]) -> pd.DataFrame:
        df = pd.concat([Extraction.__preprocess_first_df(dfs[0])] + dfs[1:])
        df.columns = ["nome_aluno", "disciplina_1", "disciplina_2", "disciplina_3"]
        return df


def extract_raw_pdf():
    PDF_PATH: str = "data/raw/ResultadoAE20211.pdf"
    ext = Extraction(PDF_PATH)
    df = ext.extract()
    df.to_csv("data/interim/alunos.csv", index=False)


if __name__ == "__main__":
    extract_raw_pdf()

import pandas as pd


def join_all_data():
    students = pd.read_csv("data/interim/alunos_cursos.csv")
    courses = pd.read_json(
        "data/interim/cursos.json", encoding="cp1252", dtype={"area_concentracao": str}
    ).dropna()
    concentration_area = pd.read_json(
        "data/interim/areas_concentracao.json",
        encoding="cp1252",
        orient="records",
        dtype={"area_concentracao": str},
    ).dropna()

    return students.merge(
        right=courses,
        on=["codigo_curso"],
        how="inner",
    ).merge(right=concentration_area, on=["area_concentracao"], how="inner")


if __name__ == "__main__":
    df = join_all_data()
    df.to_csv("data/processed/aprovacoes.csv", index=False)

import pandas as pd

from special_students.settings import settings


def join_all_data():
    students = pd.read_csv(settings.interim_students_courses_path)
    courses = pd.read_json(
        settings.interim_courses_json_path,
        encoding="cp1252",
        dtype={"area_concentracao": str},
    ).dropna()
    concentration_area = pd.read_json(
        settings.interim_concentration_areas_json_path,
        encoding="cp1252",
        orient="records",
        dtype={"area_concentracao": str},
    ).dropna()

    return students.merge(
        right=courses,
        on=["codigo_curso"],
        how="inner",
    ).merge(right=concentration_area, on=["area_concentracao"], how="inner")


def build_features():
    join_all_data().to_csv(settings.processed_approvals_path, index=False)


if __name__ == "__main__":
    build_features()

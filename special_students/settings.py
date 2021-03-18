from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    raw_pdf_path: str = "data/raw/ResultadoAE20211.pdf"
    interim_students_path: str = "data/interim/alunos.csv"
    interim_students_courses_path: str = "data/interim/alunos_cursos.csv"
    interim_courses_json_path: str = "data/interim/cursos.json"
    interim_concentration_areas_json_path: str = "data/interim/areas_concentracao,json"

    courses_columns: List[str] = ["disciplina_1", "disciplina_2", "disciplina_3"]


settings = Settings()

from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    raw_pdf_path: str = "data/raw/ResultadoAE20211.pdf"
    interim_students_path: str = "data/interim/alunos.csv"
    interim_students_courses_path: str = "data/interim/alunos_cursos.csv"

    courses_columns: List[str] = ["disciplina_1", "disciplina_2", "disciplina_3"]


settings = Settings()

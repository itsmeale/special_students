import asyncio
import json

import pandas as pd
from codetiming import Timer

from special_students.scraping.spiders import (
    SpiderGetConcentrationAreaData,
    SpiderGetCourseData,
)


def get_courses():
    df = pd.read_csv("data/interim/alunos_cursos.csv")
    return df["codigo_curso"].drop_duplicates().values


def generate_courses_data_tasks(courses):
    spider = SpiderGetCourseData()

    return [
        asyncio.create_task(spider.collect(course, "data/interim/cursos.json"))
        for course in courses
    ]


async def generate_concentration_area_data():
    spider = SpiderGetConcentrationAreaData()
    with open("data/interim/areas_concentracao.json", "w") as concentrarion_area_json:
        spider_result = await spider.collect()
        concentration_areas = json.dumps(spider_result)
        concentrarion_area_json.write(concentration_areas)


async def main():
    courses = get_courses()
    await asyncio.gather(
        *generate_courses_data_tasks(courses),
        asyncio.create_task(generate_concentration_area_data())
    )


if __name__ == "__main__":
    with Timer("Executing time: %.2f s"):
        asyncio.run(main())

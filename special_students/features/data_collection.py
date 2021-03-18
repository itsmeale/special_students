import asyncio
import json

import pandas as pd

from special_students.scraping.spiders import (SpiderGetConcentrationAreaData,
                                               SpiderGetCourseData)
from special_students.settings import settings


def get_courses():
    df = pd.read_csv(settings.interim_students_courses_path)
    return df["codigo_curso"].drop_duplicates().values


def generate_courses_data_tasks(courses):
    spider = SpiderGetCourseData()

    return [
        asyncio.create_task(spider.collect(course, settings.interim_courses_json_path))
        for course in courses
    ]


async def generate_concentration_area_data():
    spider = SpiderGetConcentrationAreaData()
    with open(
        settings.interim_concentration_areas_json_path, "w"
    ) as concentrarion_area_json:
        spider_result = await spider.collect()
        concentration_areas = json.dumps(spider_result)
        concentrarion_area_json.write(concentration_areas)


async def gather_tasks():
    courses = get_courses()
    await asyncio.gather(
        *generate_courses_data_tasks(courses),
        asyncio.create_task(generate_concentration_area_data())
    )


def data_collection():
    asyncio.run(gather_tasks())


if __name__ == "__main__":
    data_collection()

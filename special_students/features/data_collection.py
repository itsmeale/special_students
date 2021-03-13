import json

import pandas as pd

from special_students.scraping.spiders import (SpiderGetConcentrationAreaData,
                                               SpiderGetCourseData)


def get_courses():
    df = pd.read_csv("data/interim/alunos_cursos.csv")
    return df["codigo_curso"].drop_duplicates().values


def generate_courses_data(courses):
    spider = SpiderGetCourseData()
    data = []
    for course in courses:
        data.append(spider.collect(course))

    with open("data/interim/cursos.json", "w") as course_json:
        course_json.write(json.dumps(data))


def generate_concentration_area_data():
    spider = SpiderGetConcentrationAreaData()
    with open("data/interim/areas_concentracao.json", "w") as concentrarion_area_json:
        concentrarion_area_json.write(json.dumps(spider.collect()))


if __name__ == "__main__":
    courses = get_courses()
    generate_courses_data(courses)
    generate_concentration_area_data()
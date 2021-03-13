import json
from abc import ABC, abstractclassmethod
from typing import Dict

import requests as req
from bs4 import BeautifulSoup

COURSE_BASE_URL: str = (
    "https://uspdigital.usp.br/janus/Disciplina?sgldis={course_code}&origem=C&"
)

CONCENTRATION_AREA_BASE_URL: str = (
    "https://uspdigital.usp.br/janus/AreaListaPublico?codcpg=100&tipo=D&origem=C&"
)


class Spider(ABC):
    @abstractclassmethod
    def collect(self) -> Dict:
        raise NotImplementedError("Collect class not implemented.")

    @staticmethod
    def get_page_soup(url: str):
        return BeautifulSoup(req.get(url).text, features="html.parser")

    @staticmethod
    def get_course_page(course_code: str) -> str:
        return req.get(COURSE_BASE_URL.format(course_code=course_code)).text

    @staticmethod
    def get_course_page_soup(course_code):
        return BeautifulSoup(
            Spider.get_course_page(course_code), features="html.parser"
        )


class SpiderGetCourseData(Spider):
    @staticmethod
    def extract_data(info_field: str) -> str:
        return info_field.split(":")[1].strip()

    @staticmethod
    def data_exists(soup: BeautifulSoup):
        return True if soup.find("p", {"class": "info infopt"}) else False

    def collect(self, course_code: str) -> Dict:
        soup = Spider.get_course_page_soup(course_code)

        if not SpiderGetCourseData.data_exists(soup):
            return {
                "codigo_curso": None,
                "nome_curso": None,
                "area_concentracao": None,
                "creditos": None,
            }

        head_info = soup.find_all("span", {"class": "infopt"})
        infos = soup.find_all("p", {"class": "info infopt"})
        infos = [info.get_text() for info in infos]

        concentration_area = SpiderGetCourseData.extract_data(infos[0])
        credits = SpiderGetCourseData.extract_data(infos[3])

        return {
            "codigo_curso": course_code,
            "nome_curso": head_info[1].get_text().strip().upper(),
            "area_concentracao": concentration_area,
            "creditos": credits,
        }


class SpiderGetConcentrationAreaData(Spider):
    def collect(self) -> Dict:
        def clear_text(text: str) -> str:
            return text.strip().upper()

        soup = Spider.get_page_soup(CONCENTRATION_AREA_BASE_URL)
        areas_links = soup.find_all("a")

        areas = [
            list(map(clear_text, area.get_text().split("-"))) for area in areas_links
        ][1:]

        return [
            {"area_concentracao": area[0], "nome_area_concentracao": area[1]}
            for area in areas
        ]


if __name__ == "__main__":
    spider = SpiderGetCourseData()
    data = spider.collect("SCX5002")
    print(data)

    spider_concentration = SpiderGetConcentrationAreaData()
    with open("concentration_area.json", "w") as concentration_json:
        concentration_json.write(json.dumps(spider_concentration.collect()))

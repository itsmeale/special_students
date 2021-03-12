import requests as req
from bs4 import BeautifulSoup

from abc import ABC, abstractclassmethod


COURSE_BASE_URL: str = (
    "https://uspdigital.usp.br/janus/Disciplina?sgldis={course_code}&origem=C&"
)


class Spider(ABC):
    @abstractclassmethod
    def collect(self):
        raise NotImplementedError("Collect class not implemented.")

    def get_course_page(course_code: str) -> str:
        return req.get(COURSE_BASE_URL.format(course_code=course_code)).text

    def get_course_page_soup(course_code):
        return BeautifulSoup(
            Spider.get_course_page(course_code), features="html.parser"
        )


class SpiderGetCourseData(Spider):
    def __init__(self, course: str):
        self.course_code = course

    @staticmethod
    def extract_data(info_field: str) -> str:
        return info_field.split(":")[1].strip()

    def collect(self):
        soup = Spider.get_course_page_soup(self.course_code)
        head_info = soup.find_all("span", {"class": "infopt"})
        infos = soup.find_all("p", {"class": "info infopt"})
        infos = [info.get_text() for info in infos]

        concentration_area = SpiderGetCourseData.extract_data(infos[0])
        credits = SpiderGetCourseData.extract_data(infos[3])

        return {
            "course_code": self.course_code,
            "course_name": head_info[1].get_text().strip().upper(),
            "concentration_area": concentration_area,
            "credits": credits,
        }


if __name__ == "__main__":
    spider = SpiderGetCourseData("SCX5002")
    data = spider.collect()
    print(data)

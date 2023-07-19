from abc import ABC, abstractmethod
import requests
import os


class JobSiteAPI(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями """

    @abstractmethod
    def get_vacancies(self, keyword) -> dict:
        """Возвращает отфильтрованные по ключевому слову вакансии с сайта """
        pass

    @staticmethod
    def clean_vacancies(data) -> list:
        """Приводит данные к единому стандарту """
        pass


class HeadHunterAPI(JobSiteAPI):
    """Класс для работы с API сайта с вакансиями: hh.ru """

    def __init__(self):
        """Создание экземпляра класса HeadHunterAPI"""
        self.url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, keyword) -> dict:
        """Возвращает отфильтрованные по ключевому слову вакансии с сайта """
        params = {
            "text": keyword,  # ключевое слово фильтра
            "area": 1,  # город поиска работы(1 - Москва)
            "per_page": 50,  # количество вакансий
        }
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(f"Request failed with status code: {response.status_code}")

    @staticmethod
    def clean_vacancies(data) -> list:
        """Приводит данные к единому стандарту """
        clean_vacancies = []
        vacancies = data.get("items", [])
        for vacancy in vacancies:
            vacancy_title = vacancy.get("name")
            vacancy_url = vacancy.get("alternate_url")
            try:
                vacancy_salary_from = vacancy.get("salary", {}).get("from")
                if vacancy_salary_from is None:
                    vacancy_salary_from = 0
            except AttributeError:
                vacancy_salary_from = 0
            vacancy_employer = vacancy.get("employer", {}).get("name")

            clean_vacancies.append({"title": vacancy_title,
                                    "url": vacancy_url,
                                    "salary_from": vacancy_salary_from,
                                    "employer": vacancy_employer})

        return clean_vacancies


class SuperJobAPI(JobSiteAPI):
    """Класс для работы с API сайта с вакансиями: superjob.ru """

    def __init__(self):
        """Создание экземпляра класса SuperJobAPI"""
        self.url = "https://api.superjob.ru/2.0/vacancies/"
        self.headers = {
            'X-Api-App-Id': os.getenv('API_KEY'),
        }

    def get_vacancies(self, keyword) -> dict:
        """Возвращает отфильтрованные по ключевому слову вакансии с сайта """

        params = {
            "keyword": keyword,  # ключевое слово фильтра
            "town": 4,  # номер региона (4 - Москва)
            "count": 50,  # количество вакансий
        }
        response = requests.get(self.url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(f"Request failed with status code: {response.status_code}")

    @staticmethod
    def clean_vacancies(data) -> list:
        """Приводит данные к единому стандарту """

        clean_vacancies = []
        vacancies = data.get("objects", [])
        for vacancy in vacancies:
            vacancy_title = vacancy.get("profession")
            vacancy_url = vacancy.get("link")
            vacancy_salary_from = vacancy.get("payment_from")
            vacancy_employer = vacancy.get("client", {}).get("title")

            clean_vacancies.append({"title": vacancy_title,
                                    "url": vacancy_url,
                                    "salary_from": vacancy_salary_from,
                                    "employer": vacancy_employer})

        return clean_vacancies
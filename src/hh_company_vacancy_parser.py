from pprint import pprint
from typing import Any
import requests


class HHVacancionParsing:
    def __init__(self, name=None):
        """
        Инициализация класса HHVacancionParsing.

        :param name: Список названий компаний для поиска. Если не указано, будут возвращены компании по умолчанию.
        """
        self.name = name

    @property
    def get_request_employeers(self) -> list[Any]:
        """
        Метод, возвращающий список работодателей (компаний).
        По умолчанию возвращает 10 компаний, если имя не указано.

        :return: Список работодателей в формате JSON.
        """
        list_employeers = []

        # Если имя не указано, возвращаем 10 компаний по умолчанию
        if self.name is None:
            params = {
                "per_page": 10,
                "sort_by": "by_vacancies_open",
            }
            response = requests.get("http://api.hh.ru/employers/", params)
            return response.json()["items"]

        # Если имена указаны, получаем компании по каждому имени
        else:
            for i in self.name:
                params = {
                    "per_page": 10,
                    "sort_by": "by_vacancies_open",
                    "text": i
                }
                response = requests.get("http://api.hh.ru/employers/", params)
                list_employeers.extend(response.json()["items"])

        return list_employeers

    def get_employers_sort(self) -> list:
        """
        Метод сортировки работодателей.
        Возвращает список с id компании и названием.

        :return: Отсортированный список работодателей.
        """
        result = self.get_request_employeers
        employers = []
        for employer in result:
            employers.append({"id": int(employer["id"]), "name": employer["name"]})
        return employers

    @classmethod
    def get_vacancies_from_company(cls, id_company) -> str:
        """
        Метод для получения вакансий из компании по ее ID.

        :param id_company: ID компании, для которой нужно получить вакансии.
        :return: Список вакансий в формате JSON.
        """
        params = {
            "per_page": 20,
            "employer_id": id_company,
            'only_with_salary': "true"  # Фильтруем вакансии только с указанием зарплаты
        }
        response = requests.get("http://api.hh.ru/vacancies/", params)
        return response.json()["items"]

    def get_all_vacancyes(self) -> list:
        """
        Получение всех вакансий из всех компаний.

        :return: Список всех вакансий.
        """
        employers = self.get_employers_sort()  # Получаем отсортированных работодателей
        vacancies = []
        for employer in employers:
            vacancies.extend(self.get_vacancies_from_company(employer["id"]))  # Получаем вакансии по каждой компании
        return vacancies

    def filter_vacancyes(self) -> list:
        """
        Фильтрация вакансий, приводящая их в более удобный вид.

        :return: Список вакансий с отфильтрованной информацией.
        """
        vacancies = self.get_all_vacancyes()  # Получаем все вакансии
        filter_vacancy = []

        # Фильтруем вакансии для удобного представления
        for vacancy in vacancies:
            if vacancy["salary"]["from"] is None:
                vacancy["salary"]["from"] = 0  # Устанавливаем минимальную зарплату в 0, если она None
            if vacancy["salary"]["to"] is None:
                vacancy["salary"]["to"] = 0  # Устанавливаем максимальную зарплату в 0, если она None

            # Добавляем отфильтрованную информацию о вакансии в список
            filter_vacancy.append({
                "id": int(vacancy["id"]),
                "name": vacancy["name"],
                "salary_from": vacancy["salary"]["from"],
                "salary_to": vacancy["salary"]["to"],
                "url": vacancy["alternate_url"],
                "employer": int(vacancy["employer"]["id"]),

                "employer_name": vacancy["employer"]["name"]
            })
        return filter_vacancy

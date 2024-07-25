import psycopg2
from src.hh_company_vacancy_parser import HHVacancionParsing
from config import config


class DBModule:

    def __init__(self, db_name):
        """
        Инициализация класса DBModule и подключение к базе данных.

        :param db_name: Имя базы данных, к которой нужно подключиться.
        """
        self.db_name = db_name
        self.conn = psycopg2.connect(dbname=self.db_name, **config())  # Устанавливаем соединение с БД

    def create_tables(self) -> None:
        """
        Метод создает две таблицы в базе данных 'hh_vacancies'.
        Одна таблица называется 'employer', вторая 'vacancies'.

        - Таблица 'employer':
            - employer_id (int, PRIMARY KEY)
            - employer_name (varchar(150))

        - Таблица 'vacancies':
            - vacancy_id (int, PRIMARY KEY)
            - company_id (int, FOREIGN KEY к employer_id в таблице 'employer')
            - vacancy_name (varchar(250), NOT NULL)
            - salary_from (int)
            - salary_to (int)
            - url (varchar(250))
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                # Создаем таблицу employer
                cursor.execute('CREATE TABLE employer('
                               'employer_id int PRIMARY KEY,'
                               'employer_name varchar(150));')

                # Создаем таблицу vacancies
                cursor.execute('CREATE TABLE vacancies('
                               'vacancy_id int PRIMARY KEY,'
                               'company_id int REFERENCES employer(employer_id),'
                               'vacancy_name varchar(250) NOT NULL,'
                               'salary_from int,'
                               'salary_to int,'
                               'url varchar(250));')

    def full_tables(self, value) -> None:
        """
        Записываем компании и вакансии из сайта HH в соответствующие таблицы базы данных.

        :param value: Список названий компаний, для которых нужно получить вакансии.
        """
        head_hunter = HHVacancionParsing(value)  # Инициализируем парсер вакансий
        employers = head_hunter.get_employers_sort()  # Получаем отсортированный список работодателей
        vacancies = head_hunter.filter_vacancyes()  # Получаем фильтрованные вакансии

        with self.conn:
            with self.conn.cursor() as cur:
                # Записываем данные о работодателях в таблицу employer
                for employer in employers:
                    cur.execute("""
                                    INSERT INTO employer VALUES (%s, %s)
                                """, (employer["id"], employer["name"]))

                # Записываем данные о вакансиях в таблицу vacancies
                for vacancy in vacancies:
                    cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                                (vacancy["id"], vacancy["employer"], vacancy["name"], vacancy["salary_from"],
                                 vacancy["salary_to"], vacancy["url"]))


if __name__ == '__main__':
    hh = DBModule('python')  # Создаем экземпляр DBModule для базы данных 'python'

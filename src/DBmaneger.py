import psycopg2
from config import config


class DBManager:

    def __init__(self, db_name):
        """
        Инициализация класса DBManager и подключение к базе данных.

        :param db_name: Имя базы данных, к которой нужно подключиться.
        """
        self.db_name = db_name
        self.conn = psycopg2.connect(dbname=self.db_name, **config())  # Устанавливаем соединение с БД

    def get_companies_and_vacancies_count(self) -> None:
        """
        Получаем список всех компаний и количество вакансий у каждой компании.
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                # SQL-запрос для получения имен работодателей и количества их вакансий
                cursor.execute('SELECT employer.employer_name, COUNT(vacancies.company_id) AS vacancies_count '
                               'FROM employer LEFT JOIN vacancies ON employer.employer_id = vacancies.company_id '
                               'GROUP BY employer.employer_name')
                resulting = cursor.fetchall()  # Получаем все результаты запроса
                self.conn.commit()  # Фиксируем изменения, хотя для SELECT это не обязательно
                print(resulting)  # Выводим результаты

    def get_all_vacancies(self) -> None:
        """
        Получает список всех вакансий с названием вакансии, зарплаты и ссылкой на вакансию.
        """
        with self.conn.cursor() as cursor:
            # SQL-запрос для получения всех вакансий с именем работодателя
            cursor.execute('SELECT employer.employer_name, vacancies.vacancy_name, '
                           'vacancies.salary_from, vacancies.salary_to '
                           'FROM vacancies JOIN employer ON employer.employer_id = vacancies.company_id '
                           'ORDER BY employer_name')
            resulting = cursor.fetchall()  # Получаем все результаты запроса
            self.conn.commit()  # Фиксируем изменения
            print(resulting)  # Выводим результаты

    def get_avg_salary(self) -> None:
        """
        Получаем среднюю зарплату по вакансиям.
        """
        with self.conn.cursor() as cursor:
            # SQL-запрос для получения средней зарплаты
            cursor.execute("SELECT AVG(salary_from) AS payment_avg FROM vacancies")
            resulting = cursor.fetchall()  # Получаем результаты запроса
            self.conn.commit()  # Фиксируем изменения
            print(resulting)  # Выводим результаты

    def get_vacancies_with_higher_salary(self) -> None:
        """
        Список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        with self.conn.cursor() as cursor:
            # SQL-запрос для получения вакансий с зарплатой выше средней
            cursor.execute("SELECT vacancy_name, salary_from, url FROM vacancies "
                           "WHERE salary_from > (SELECT AVG(salary_from) "
                           "FROM vacancies)")
            resulting = cursor.fetchall()  # Получаем результаты запроса
            self.conn.commit()  # Фиксируем изменения
            print(resulting)  # Выводим результаты

    def get_vacancies_with_keyword(self, keyword) -> None:
        """
        Получаем список всех вакансий, в названии которых содержатся переданные слова, например 'Руководитель'.

        :param keyword: Ключевое слово, по которому будет производится поиск в названиях вакансий.
        """
        with self.conn.cursor() as cursor:
            # SQL-запрос для получения вакансий по ключевому слову
            cursor.execute(f"SELECT * FROM vacancies WHERE vacancy_name LIKE \'%{keyword}%\'")
            resulting = cursor.fetchall()  # Получаем результаты запроса
            self.conn.commit()  # Фиксируем изменения
            print(resulting)  # Выводим результаты


if __name__ == '__main__':
    result = DBManager('python')  # Создаем экземпляр DBManager для базы данных 'python'

    result.get_vacancies_with_keyword('Руководитель')  # Получаем вакансии с ключевым словом 'Руководитель'

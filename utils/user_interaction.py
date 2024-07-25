import psycopg2
from src.hh_company_vacancy_parser import HHVacancionParsing
from src.DBmodul import DBModule
from config import config


def user_interaction(value, db_name) -> None:
    """
    Получает данные от пользователя, записывает их в базу данных
    и сортирует.

    :param value: Данные, полученные от пользователя для обработки.
    :param db_name: Название базы данных, в которую будут записываться данные.
    """
    # Обработка данных от пользователя с помощью парсера вакансий
    HHVacancionParsing(value)

    # Создание экземпляра модуля работы с базой данных
    module = DBModule(db_name)

    # Создание таблиц в базе данных
    module.create_tables()

    # Заполнение таблиц данными
    module.full_tables(value)


def delete_database(database_name: str) -> None:
    """
    Удаляет указанную базу данных.

    :param database_name: Название базы данных, которую нужно удалить.
    """
    # Устанавливаем соединение с базой данных PostgreSQL
    conn = psycopg2.connect(dbname='postgres', **config())
    conn.autocommit = True  # Включаем автоматическое подтверждение транзакций
    cur = conn.cursor()  # Создаем курсор для выполнения операций с БД

    # Выполняем команду на удаление базы данных
    cur.execute(f'DROP DATABASE {database_name}')

    cur.close()  # Закрываем курсор
    conn.close()  # Закрываем соединение


def create_database(database_name: str) -> None:
    """
    Создает новую базу данных.

    :param database_name: Название базы данных, которую нужно создать.
    """
    # Устанавливаем соединение с базой данных PostgreSQL
    conn = psycopg2.connect(dbname='postgres', **config())
    conn.autocommit = True  # Включаем автоматическое подтверждение транзакций
    cur = conn.cursor()  # Создаем курсор для выполнения операций с БД

    # Выполняем команду на создание новой базы данных
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()  # Закрываем курсор
    conn.close()  # Закрываем соединение


if __name__ == '__main__':
    # Удаляем базу данных с именем 'python'
    delete_database('python')

from utils.user_interaction import user_interaction, delete_database, create_database
from src.DBmaneger import DBManager

# Запрос имени базы данных у пользователя
db_name = input('Введите название базы данных\n')

# Создание базы данных
create_database(db_name)

# Инициализация менеджера базы данных
db_manager = DBManager(db_name)

# Запрос названий компаний у пользователя
user_input = input("Введите название компаний через запятую, для просмотра!\n"
                   "Если не указать вакансии, по умолчанию программа вернет 10 первых\n").split(',')

# Взаимодействие с пользователем для сохранения компании в базе данных
user_interaction(user_input, db_name)
print('Список Компаний сохранен в базе данных!\n')

try:
    while True:
        # Показ меню для выбора действия
        print("Выберите число от 1 до 5:\n"
              "1. Получить список всех компаний и количество вакансий у каждой компании.\n"
              "2. Получить список всех вакансий с указанием названия компании, названия вакансии, "
              "зарплаты и ссылки на вакансию.\n"
              "3. Получить среднюю зарплату по вакансиям.\n"
              "4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
              "5. Получить список всех вакансий, в названии которых содержатся переданные "
              "в метод слова, например 'python'.\n")

        # Ввод номера действия от пользователя
        number_user = input().strip()

        # Выполнение действий в зависимости от ввода пользователя
        if number_user == '1':
            db_manager.get_companies_and_vacancies_count()
        elif number_user == '2':
            db_manager.get_all_vacancies()
        elif number_user == '3':
            db_manager.get_avg_salary()
        elif number_user == '4':
            db_manager.get_vacancies_with_higher_salary()
        elif number_user == '5':
            word_user = input("Введите слово для поиска вакансий\n")
            db_manager.get_vacancies_with_keyword(word_user)
        else:
            exit_user = input("Вы ввели неверные данные:\n"
                              "введите 'exit' для выхода, или повторите ввод\n").strip()
            if exit_user == 'exit':
                break
            else:
                continue

        # Запрос на продолжение работы программы
        user_question = input("Желаете продолжить: 1-ДА, 2-НЕТ\n").strip()
        if user_question == '1':
            continue
        else:
            break
finally:
    # Закрытие соединения с базой данных и удаление базы данных после завершения
    db_manager.conn.close()
    print("Удаление данных с базы данных!\n")
    delete_database(db_name)
    print("Всего хорошего!")

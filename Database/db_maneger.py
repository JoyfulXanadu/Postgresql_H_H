import psycopg2


class DBManager:
    def __init__(self, db_config):
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self):
        self.cursor.execute("SELECT name, vacancies_count FROM companies;")
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        self.cursor.execute("""
            SELECT companies.name, vacancies.title, vacancies.salary, vacancies.link 
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id;
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        self.cursor.execute("SELECT AVG(salary) FROM vacancies;")
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cursor.execute("""
            SELECT companies.name, vacancies.title, vacancies.salary 
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
            WHERE vacancies.salary > %s;
        """, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cursor.execute("""
            SELECT companies.name, vacancies.title, vacancies.salary 
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
            WHERE vacancies.title ILIKE %s;
        """, (f"%{keyword}%",))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()


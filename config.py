from configparser import ConfigParser
from path_database import FILE


def config(filename=FILE, section="postgresql"):
    """
    Читает конфигурационный файл и возвращает параметры подключения к базе данных.

    :param filename: Строка, путь к файлу конфигурации (по умолчанию FILE).
    :param section: Строка, название секции в конфигурационном файле (по умолчанию "postgresql").
    :return: Словарь с параметрами подключения к базе данных.
    :raises Exception: Если секция не найдена в файле конфигурации.
    """

    # Создание объекта парсера для конфигурационного файла
    parser = ConfigParser()

    # Чтение конфигурационного файла
    parser.read(filename)

    # Создание словаря для хранения параметров подключения
    db = {}

    # Проверка наличия указанной секции в конфигурационном файле
    if parser.has_section(section):
        # Получение всех параметров из указанной секции
        params = parser.items(section)

        # Заполнение словаря параметрами подключения
        for param in params:
            db[param[0]] = param[1]
    else:
        # Выбрасывание исключения, если секция не найдена
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))

    return db

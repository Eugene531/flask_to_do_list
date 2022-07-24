from db_init import db
from config import t_name


def get_data_from_db():
    """Берет все данные из базы и возвращает их в формате json.

    Процесс преобразования:
    При экспорте всех данных из БД они предстают в формате списка кортежей.
    Чтобы преобразовать экспортированные данные в json формат, используется функция
    map в сочетании со вложенной функцией to_json. Функция to_json принимает
    в качестве параметра один элемент списка и возвращает словарь, где ключ - это
    id, а значение - это множество параметров: title, text, date и progress.
    """
    def to_json(db_data):
        return {
            str(db_data[0]):
                {
                'title': db_data[1],
                'text': db_data[2],
                'date': db_data[3],
                'progress': db_data[4],
                }
        }
    result = db.engine.execute(f"SELECT * FROM {t_name}").fetchall()
    result = map(to_json, result)
    json_data_from_db = {}
    for res in result:
        json_data_from_db.update(res)
    return json_data_from_db

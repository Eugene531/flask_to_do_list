from flask import jsonify, request

from db_init import db, ToDoListTable
from config import t_name
from helpful_fun import get_data_from_db
from app import app


@app.route('/todolist/add_task', methods=['POST'])
def add_task():
    """Создает новую задачу (task) и помещает ее в базу данных.

    Процесс создания задачи:
    Для создания новой задачи используется метод POST, в котором передаются данные
    в формате json, это обязательно (не больше и неменьше) три параметра: title,
    text и date, соответственно: заголовок, текст задачи и дата выполнения.
    Здесь title и text могут содержать любые символы, включая пустые строки, а параметр
    date должен содержать данные в формате: "ДД.ММ.ГГГГ".

    Возможные ошибочные ситуации и их обработка:
    1) если данных в запросе больше трех;
    2) если данных в запросе меньше трех;
    3) если дата была передана не в верном формате.
    То, возвращается json ответ с описанием соответствующей ошибки и код 404.
    """
    try:
        res = request.json
        if len(res) > 3:
            return jsonify({'Error': 'Extra data in req, needed: title, text, date'}), 404
        title, text, date = res['title'], res['text'], res['date']
        new_task = ToDoListTable(title=title, text=text, date=date)
        db.session.flush()
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'Successful': 'Completed add!'})
    except:
        db.session.rollback()
        return jsonify({'Error': 'Some parameters are incorrect'}), 404
    finally:
        db.session.close()


@app.route('/todolist/get_tasks', methods=['GET'])
def get_all_tasks():
    """Берет все данные из базы и возвращает их в формате json.
    Если данных в БД нет, то вернет json предупреждение об этом
    """
    data_from_db = get_data_from_db()
    if not data_from_db:
        return jsonify({'Info': 'The database does not contain a single task'})
    return jsonify(data_from_db)


@app.route('/todolist/get_task/<string:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    """Берет все данные одной задачи из базы по id и возвращает их в формате json.
    Если переданного id нет в БД, то вернет ошибку с ее описанием и кодом 404
    """
    data_from_db = get_data_from_db()
    if data_from_db.get(task_id, False):
        return jsonify(data_from_db.get(task_id))
    return jsonify({'Error 404': f"Task with id {task_id} doesn't exist"}), 404


@app.route('/todolist/set_progress/<string:task_id>', methods=['PUT'])
def set_progress(task_id):
    """Устанавливает прогресс задачи как выполненный (т.е. true) по переданному id.
    Если переданного id нет в БД, то вернет ошибку с ее описанием и кодом 404
    """
    data_from_db = get_data_from_db()
    if data_from_db.get(task_id, False):
        db.engine.execute(f"UPDATE {t_name} SET progress = true WHERE id = {task_id}")
        return jsonify({'Successful': 'Completed set!'})
    return jsonify({'Error 404': f"Task with id {task_id} doesn't exist"}), 404


# Удаление задачи
@app.route('/todolist/delete_task/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Удаляет задачу по переданному id.
    Если переданного id нет в БД, то вернет ошибку с ее описанием и кодом 404
    """
    data_from_db = get_data_from_db()
    if data_from_db.get(task_id, False):
        db.engine.execute(f"DELETE FROM {t_name} WHERE id = {task_id}")
        return jsonify({'Successful': 'Completed delete!'})
    return jsonify({'Error 404': f"Task with id {task_id} doesn't exist"}), 404


if __name__ == '__main__':
    app.run(debug=True)

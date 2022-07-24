import unittest


def setUpModule():
    """Перед выполнением модуля перезаписываю файл config.py следующим образом:
    t_name = 'test_to_do_list_table'
    db_name = 'test_to_do_list_db'
    """
    old_config_data = []
    with open('config.py', 'r') as file:
        for data in file:
            old_config_data += [data]
    with open('config.py', 'w') as file:
        for data in old_config_data:
            cash = "t_name = 'test_to_do_list_table'\n" if "t_name" in data else data
            file.write("db_name = 'test_to_do_list_db'\n" if 'db_name' in cash else cash)


def tearDownModule():
    """После выполнением модуля перезаписываю файл config.py следующим образом:
    t_name = 'to_do_list_table'
    db_name = 'to_do_list_db'

    Т.е. возвращаю изначальное содержимое файла конфигурации.
    """
    old_config_data = []
    with open('config.py', 'r') as file:
        for data in file:
            old_config_data += [data]
    with open('config.py', 'w') as file:
        for data in old_config_data:
            cash = "t_name = 'to_do_list_table'\n" if "t_name" in data else data
            file.write("db_name = 'to_do_list_db'\n" if 'db_name' in cash else cash)


class TestWithEmptyDB(unittest.TestCase):
    def setUp(self):
        import routes

        self.app = routes.app.test_client()
        routes.app.config['TESTING'] = True

    def test_get_all_tasks_from_empty_db(self):
        """Тест запроса GET на получение всех данных из пустой базы данных"""
        response = self.app.get('/todolist/get_tasks')
        expected = '{"Info":"The database does not contain a single task"}'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_get_task_from_empty_db(self):
        """Тест запроса GET на получение данных одной задачи из пустой базы данных"""
        response = self.app.get('/todolist/get_task/1')
        expected = '{"Error 404":"Task with id 1 doesn\'t exist"}'
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_set_progress_from_empty_db(self):
        """Тест запроса PUT на установление прогресса задачи в пустой базе данных"""
        response = self.app.put('/todolist/set_progress/1')
        expected = '{"Error 404":"Task with id 1 doesn\'t exist"}'
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_delete_task_from_empty_db(self):
        """Тест запроса DELETE на удаление задачи в пустой базе данных"""
        response = self.app.delete('/todolist/delete_task/1')
        expected = '{"Error 404":"Task with id 1 doesn\'t exist"}'
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_add_task_with_extra_data(self):
        """Тест запроса POST на добавление задачи с лишними данными"""
        response = self.app.post('/todolist/add_task',
                                 json={'title': 'title1', 'text': 'text1', 'date': '22.09.2022', 'extra': '123'}
                                 )
        expected = '{"Error":"Extra data in req, needed: title, text, date"}'
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_add_task_with_incorrect_date(self):
        """Тест запроса POST на добавление задачи с неверной датой"""
        response = self.app.post('/todolist/add_task',
                                 json={'title': 'title1', 'text': 'text1', 'date': 'not_date'}
                                 )
        expected = '{"Error":"Some parameters are incorrect"}'
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_add_task_with_out_some_data(self):
        """Тест запроса POST на добавление задачи без параметров text и date"""
        response = self.app.post('/todolist/add_task',
                                 json={'title': 'title1'}
                                 )
        expected = '{"Error":"Some parameters are incorrect"}'
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_add_task_with_out_data(self):
        """Тест запроса POST на добавление задачи с пустым json-ом"""
        response = self.app.post('/todolist/add_task',
                                 json={}
                                 )
        expected = '{"Error":"Some parameters are incorrect"}'
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def tearDown(self):
        pass


class TestWithNotEmptyDB(unittest.TestCase):
    def setUp(self):
        import routes

        self.app = routes.app.test_client()
        routes.app.config['TESTING'] = True

    def test_add_task(self):
        """Тест на корректное добавление задачи"""
        response = self.app.post('/todolist/add_task',
                                 json={'title': 'title1', 'text': 'text1', 'date': '24.07.2022'}
                                 )
        expected = '{"Successful":"Completed add!"}'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_add_task_with_empty_data(self):
        """Тест на корректное добавление задачи с пустыми title и text"""
        response = self.app.post('/todolist/add_task',
                                 json={'title': '', 'text': '', 'date': '20.01.2001'}
                                 )
        expected = '{"Successful":"Completed add!"}'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_get_all_tasks(self):
        """Тест на корректное получение всех задач"""
        # Add some data to db
        self.app.post('/todolist/add_task',
                      json={'title': 'title1', 'text': 'text1', 'date': '24.07.2022'}
                      )
        self.app.post('/todolist/add_task',
                      json={'title': 'title2', 'text': 'text2', 'date': '24.08.2022'}
                      )
        self.app.post('/todolist/add_task',
                      json={'title': 'title3', 'text': 'text3', 'date': '24.09.2022'}
                      )

        # Get all data from db
        response = self.app.get('/todolist/get_tasks')
        expected = '{' \
                   '"1":{"date":"Sun, 24 Jul 2022 00:00:00 GMT","progress":false,"text":"text1","title":"title1"},' \
                   '"2":{"date":"Wed, 24 Aug 2022 00:00:00 GMT","progress":false,"text":"text2","title":"title2"},' \
                   '"3":{"date":"Sat, 24 Sep 2022 00:00:00 GMT","progress":false,"text":"text3","title":"title3"}' \
                   '}'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_get_task(self):
        """Тест на корректное получение одной задачи"""
        # Add some data to db
        self.app.post('/todolist/add_task',
                      json={'title': 'title1', 'text': 'text1', 'date': '24.07.2022'}
                      )
        self.app.post('/todolist/add_task',
                      json={'title': 'title2', 'text': 'text2', 'date': '24.08.2022'}
                      )
        self.app.post('/todolist/add_task',
                      json={'title': 'title3', 'text': 'text3', 'date': '24.09.2022'}
                      )

        # Get task (with id 2)
        response = self.app.get('/todolist/get_task/2')
        expected = '{' \
                   '"date":"Wed, 24 Aug 2022 00:00:00 GMT","progress":false,"text":"text2","title":"title2"' \
                   '}'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_set_progress(self):
        """Тест на корректное установление прогресса задачи"""
        # Add some data to db
        self.app.post('/todolist/add_task',
                      json={'title': 'title1', 'text': 'text1', 'date': '24.07.2022'}
                      )
        self.app.post('/todolist/add_task',
                      json={'title': 'title2', 'text': 'text2', 'date': '24.08.2022'}
                      )
        self.app.post('/todolist/add_task',
                      json={'title': 'title3', 'text': 'text3', 'date': '24.09.2022'}
                      )

        # Set task (with id 2) progress
        response = self.app.put('/todolist/set_progress/2')
        expected = '{"Successful":"Completed set!"}'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_delete_task(self):
        """Тест на корректное удаление задачи"""
        # Add some data to db
        self.app.post('/todolist/add_task',
                      json={'title': 'title1', 'text': 'text1', 'date': '24.07.2022'}
                      )
        self.app.post('/todolist/add_task',
                      json={'title': 'title2', 'text': 'text2', 'date': '24.08.2022'}
                      )
        self.app.post('/todolist/add_task',
                      json={'title': 'title3', 'text': 'text3', 'date': '24.09.2022'}
                      )

        # Delete task (with id 2)
        response = self.app.delete('/todolist/delete_task/2')
        expected = '{"Successful":"Completed delete!"}'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_get_all_tasks_after_set_progress(self):
        """Тест на корректное получение всех задач после установки прогресса"""
        # Add some data to db
        self.app.post('/todolist/add_task',
                      json={'title': 'title1', 'text': 'text1', 'date': '24.07.2022'}
                      )
        self.app.post('/todolist/add_task',
                      json={'title': 'title2', 'text': 'text2', 'date': '24.08.2022'}
                      )
        self.app.post('/todolist/add_task',
                      json={'title': 'title3', 'text': 'text3', 'date': '24.09.2022'}
                      )

        # Set task (with id 2) progress
        self.app.put('/todolist/set_progress/2')

        # Get all data from db
        response = self.app.get('/todolist/get_tasks')
        expected = '{' \
                   '"1":{"date":"Sun, 24 Jul 2022 00:00:00 GMT","progress":false,"text":"text1","title":"title1"},' \
                   '"2":{"date":"Wed, 24 Aug 2022 00:00:00 GMT","progress":true,"text":"text2","title":"title2"},' \
                   '"3":{"date":"Sat, 24 Sep 2022 00:00:00 GMT","progress":false,"text":"text3","title":"title3"}' \
                   '}'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def test_get_all_tasks_after_delete(self):
        """Тест на корректное получение всех задач после удаления"""
        # Add some data to db
        self.app.post('/todolist/add_task',
                      json={'title': 'title1', 'text': 'text1', 'date': '24.07.2022'}
                      )
        self.app.post('/todolist/add_task',
                      json={'title': 'title2', 'text': 'text2', 'date': '24.08.2022'}
                      )
        self.app.post('/todolist/add_task',
                      json={'title': 'title3', 'text': 'text3', 'date': '24.09.2022'}
                      )

        # Delete task (with id 2)
        self.app.delete('/todolist/delete_task/2')

        # Get all data from db
        response = self.app.get('/todolist/get_tasks')
        expected = '{' \
                   '"1":{"date":"Sun, 24 Jul 2022 00:00:00 GMT","progress":false,"text":"text1","title":"title1"},' \
                   '"3":{"date":"Sat, 24 Sep 2022 00:00:00 GMT","progress":false,"text":"text3","title":"title3"}' \
                   '}'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8').splitlines()[0], expected)

    def tearDown(self):
        """Удаляем таблицу, чтобы идентификация началась с единицы"""
        import routes

        with routes.app.app_context():
            routes.db.engine.execute(f'TRUNCATE TABLE {routes.t_name} RESTART IDENTITY')


if __name__ == '__main__':
    unittest.main()

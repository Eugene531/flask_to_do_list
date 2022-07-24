from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from config import user, password, host, port, db_name, t_name
from app import app


# Инициализация конфигурационных данных
db_url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создание базы данных, если не была создана
engine = create_engine(db_url)
if not database_exists(engine.url):
    create_database(engine.url)

# Создание объекта базы данных
db = SQLAlchemy()
db.init_app(app)


class ToDoListTable(db.Model):
    """Инициализация класса, который будет описывать базу данных"""
    __tablename__ = t_name
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.TEXT)
    text = db.Column(db.TEXT)
    date = db.Column(db.DATE)
    progress = db.Column(db.BOOLEAN)

    def __init__(self, title, text, date):
        self.title = title
        self.text = text
        self.date = date
        self.progress = False

    def __repr__(self):
        return f'id: {self.id}, title: {self.title}, text: {self.text}, ' \
               f'date: {self.date}, progress: {self.progress}'


# Создание таблицы
with app.app_context():
    db.create_all()

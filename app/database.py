import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session

"""ORM - для представления таблиц в виде классов,
а с БД работать через объекты"""

# Получение данных из переменных окружения
DB_HOST = os.getenv('FSTR_DB_HOST', 'localhost')
DB_PORT = os.getenv('FSTR_DB_PORT', '5432')
DB_USER = os.getenv('FSTR_DB_LOGIN', 'postgres')
DB_PASS = os.getenv('FSTR_DB_PASS', 'password')

DB_NAME = os.getenv('FSTR_DB_NAME', 'pereval')  # Имя нашей ДБ

# Строка подключения к БД
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Создание движка для работы с БД
engine = create_engine(DATABASE_URL)

# Создание сессии БД для взаимодействия с ней
SessionLocal = sessionmaker(bind=engine)

# Создание базового класса для определения всех моделей
Base = declarative_base()


# Модель перевалов
class PerevalAdded(Base):
    __tablename__ = 'pereval_added'

    id = Column(Integer, primary_key=True, index=True)
    coord_id = Column(Integer, ForeignKey('coords_id'), nullable=False)
    status = Column(String, default='new')


# Класс для работы с БД
class Database:
    def __init__(self):
        self.session = SessionLocal()

        def add_pereval(self, coord_id: int):
            """Логика добавление нового перевала в БД"""
            new_pereval = PerevalAdded(coord_id=coord_id)
            self.session.add(new_pereval)
            self.session.commit()
            return new_pereval.id

        def close(self):
            """Закрытие сесси после создания новой записи"""
            self.session.close()

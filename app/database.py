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


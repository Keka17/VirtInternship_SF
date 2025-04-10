import os

import pendulum
from pendulum import DateTime

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

from dotenv import load_dotenv

"""ORM - для представления таблиц в виде классов,
а с БД работать через объекты"""

load_dotenv()  # Загрузка переменных окружения из .env

# Получение данных из переменных окружения
DB_HOST = os.getenv('FSTR_DB_HOST', 'localhost')
DB_PORT = os.getenv('FSTR_DB_PORT', '5432')
DB_LOGIN = os.getenv('FSTR_DB_LOGIN', 'postgres')
DB_PASS = os.getenv('FSTR_DB_PASS', 'password')

DB_NAME = os.getenv('FSTR_DB_NAME', 'pereval')  # Имя нашей ДБ
# Строка подключения к БД с использованием переменных окружения
DATABASE_URL = f'postgresql://{DB_LOGIN}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Создание движка для работы с БД
engine = create_engine(DATABASE_URL)

# Создание сессии БД для взаимодействия с ней
SessionLocal = sessionmaker(bind=engine)

# Создание базового класса для определения всех моделей
Base = declarative_base()


# Модель координат
class Coords(Base):
    __tablename__ = 'coords'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    height = Column(Integer, nullable=False)


# Модель пользователя
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fam = Column(String, nullable=False)
    name = Column(String, nullable=False)
    otc = Column(String, nullable=True)
    phone = Column(String(12), nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)

    perevals = relationship('PerevalAdded', back_populates='user')


# Модель перевалов
class PerevalAdded(Base):
    __tablename__ = 'pereval_added'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    beautytitle = Column(String(200))
    title = Column(String(200))
    other_titles = Column(String(200))
    connect = Column(Text, nullable=True)
    add_time = Column(String, nullable=False, default=pendulum.now('UTC').to_iso8601_string())
    coord_id = Column(Integer, ForeignKey('coords.id'), nullable=False)
    status = Column(String, default='new')

    # Столбцы для уровней сложности по сезонам
    winter = Column(String(2), nullable=True)
    summer = Column(String(2), nullable=True)
    autumn = Column(String(2), nullable=True)
    spring = Column(String(2), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'))  # Связь с users
    user = relationship('User', back_populates='perevals')  # Добавляем реляцию


# Создание таблицы в БД
Base.metadata.create_all(engine)


# Класс для работы с БД
class Database:
    def __init__(self):
        self.session = SessionLocal()

    def add_coords(self, latitude, longitude, height):
        """Добавление координат в БД и возврат по id"""
        new_coords = Coords(latitude=latitude,
                            longitude=longitude, height=height)

        self.session.add(new_coords)
        self.session.commit()
        return new_coords.id

    def get_or_create_user(self, fam, name, otc, phone, email):
        """Получение пользователя или создание нового"""
        user = self.session.query(User).filter(User.email == email).first()

        if not user:
            user = User(fam=fam, name=name, otc=otc, phone=phone, email=email)
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)

        return user.id  # Возвращаем ID пользователя

    def add_pereval(self, beautytitle, title, other_titles,
                        connect,  latitude, longitude, height,
                        winter, summer, autumn, spring, user_id, add_time=None
                    ):
        """Добавление нового перевала в БД """

        # Если add_time не передано, используем текущее время
        if add_time is None:
            add_time = pendulum.now('UTC').to_iso8601_string()  # Текущее время в формате ISO 8601

        # Преобразуем add_time в строку, если это объект DateTime
        if isinstance(add_time, DateTime):
            add_time = add_time.to_iso8601_string()
        # Добавляем координаты
        coord_id = self.add_coords(latitude, longitude, height)

        # Создаем новый перевал
        new_pereval = PerevalAdded(
            beautytitle=beautytitle,
            title=title,
            other_titles=other_titles,
            connect=connect,
            add_time=add_time,
            user_id=user_id,
            coord_id=coord_id,
            status='new',
            winter=winter,
            summer=summer,
            autumn=autumn,
            spring=spring
        )

        self.session.add(new_pereval)
        self.session.commit()
        return new_pereval.id

    def close(self):
        """Закрытие сесси после создания новой записи"""
        self.session.close()

import re
import os

from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Field, conlist, field_validator, EmailStr

import pendulum
from pendulum import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

from dotenv import load_dotenv

"""ORM - для представления таблиц в виде классов,
а с БД работать через объекты"""

load_dotenv()  # Загружаем переменные из .env

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
    add_time = Column(String, nullable=False)
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
            add_time = pendulum.now()  # Текущее время в формате ISO 8601

        # Преобразуем add_time в строку, если это объект datetime
        if isinstance(add_time, datetime):
            add_time = add_time.isoformat()

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


# Инизиализация FastAPI с настройками документации
app = FastAPI(
    title='API для работы с перевалами',
    description='Этот API позволяет добавлять, редактировать '
                'и получать информацию о перевалах.',
    version='1.0.0',
    docs_url='/swagger',
    redoc_url='/api-docs',
    swagger_ui_parameters={'defaultModelsExpandDepth': 1}

)


@app.get('/', summary='Проверка работоспособности API',
         description='Возвращает сообщение о том, что API работает  ')
async def root():
    return {'message': 'API работает!'}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            'detail': 'Ошибка валидации: неверно введенные данные',
            'errors': exc.errors()
        }))


class SubmitData(BaseModel):
    """Модель данных для отправки информации"""
    beautytitle: str = Field(..., min_length=1,
                             description='Заголовок для отображения на сайте')
    title: str = Field(..., min_length=1,
                       description='Основной заголовок')
    other_titles: conlist(str, min_length=0, max_length=10) = Field(default=[],
                                description='Список альтернативных названий')
    connect: str = Field(default='', description="Дополнительные сведения о связи перевала")
    add_time: datetime = Field(default_factory=pendulum.now, description='Дата и время добавления данных в UTC')
    latitude: float = Field(..., ge=-90, le=90, description='Широта в градусах')
    longitude: float = Field(..., ge=-180, le=180, description='Долгота в градусах')
    height: int = Field(..., ge=0, description='Высота в метрах над уровнем моря')

    # Поля сезонов
    winter: str = Field(..., min_length=0, max_length=2, description='Полукатегория сложности перевала зимой')
    summer: str = Field(..., min_length=0, max_length=2, description='Полукатегория сложности перевала летом')
    autumn: str = Field(..., min_length=0, max_length=2, description='Полукатегория сложности перевала осенью')
    spring: str = Field(..., min_length=0, max_length=2, description='Полукатегория сложности перевала весной')

    # Данные об авторе
    fam: str = Field(..., min_length=1, description='Фамилия автора')
    name: str = Field(..., min_length=1, description='Имя автора')
    otc: str = Field(default='', description='Отчество автора')
    phone: str = Field(..., min_length=10, max_length=12, description='Номер телефона')
    email: EmailStr

    @field_validator('add_time', mode='before')
    def validate_add_time(cls, value):
        """Строгая валидация формата даты перед конвертацией"""
        if isinstance(value, datetime):
            return value  # Если это уже datetime, возвращаем как есть

        iso_8601_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?$'

        if not isinstance(value, str) or not re.match(iso_8601_regex, value):
            raise ValueError('Ошибка: add_time должен быть в формате ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)')

        try:
            return pendulum.parse(value)  # Корректно парсим дату
        except Exception:
            raise ValueError('Ошибка парсинга даты: неверный формат ISO 8601')
def get_db():
    """Создание сесии БД для запроса и ее закрытие после использования"""
    db = Database()
    try:
        yield db  # Экземпляр db будет передан в функцию-обработчик запроса
    finally:
        db.close()  # Гарантированное закрытие сессии в любом случае


@app.post('/submitData', summary='Добавление нового перевала',
          description='Позволяет создать запись о новом перевале',
          responses={
              201: {
                  'description': 'Перевал успешно добавлен',
                  'content': {
                      'application/json': {
                          'example': {
                              'status': 'success',
                              'pereval_id': 123
                          }
                      }
                  }
              },
              422: {'description': 'Ошибка валидации: неверно введенные данные'},
              500: {'description': 'Ошибка сервера'}
          })
async def submit_data(data: SubmitData, db: Database = Depends(get_db)):
    """Обработчик POST-запроса для добавления нового перевала"""
    try:
        # Получаем или создаем пользователя
        user_id = db.get_or_create_user(
            fam=data.fam,
            name=data.name,
            otc=data.otc,
            phone=data.phone,
            email=data.email
        )

        pereval_id = db.add_pereval(
            beautytitle=data.beautytitle,
            title=data.title,
            other_titles='; '.join(data.other_titles),
            connect=data.connect,
            add_time=data.add_time.isoformat(),
            user_id=user_id,  # Передаем ID пользователя
            latitude=data.latitude,
            longitude=data.longitude,
            height=data.height,
            winter=data.winter,
            summer=data.summer,
            autumn=data.autumn,
            spring=data.spring
        )

        return {'status': 'success', 'pereval_id': pereval_id}  # JSON-ответ

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')


@app.get('/submitData/{pereval_id}', summary='Получение информации о перевале',
         description='Возвращает данные о перевале по ID',
         responses={
             200: {
                 'description': 'Информация о перевале найдена',
                 'content': {
                     'application/json': {
                         'example': {
                             'id': 1,
                             'author': 'user@example.com',
                             'beautytitle': 'Перевал Дятлова',
                             'title': 'Горный перевал',
                             'other_titles': 'Дятловский; Северный проход',
                             'connect': 'Связывает две долины',
                             'add_time': '2024-03-01T12:00:00Z',
                             'status': 'new',
                             'coords': {
                                 'latitude': 61.7581,
                                 'longitude': 59.4506,
                                 'height': 1079
                             },
                             'level': {
                                 'winter': '2А',
                                 'summer': '1Б',
                                 'autumn': '1Б',
                                 'spring': '2А'
                             }
                         }
                     }
                 }
             },
             404: {'description': 'Перевал не найден'},
             500: {'description': 'Ошибка сервера'}
         })
async def get_pereval(pereval_id: int, db: Database = Depends(get_db)):
    """Обработчик GET-запроса для получения информации о перевале по id"""
    try:
        pereval = db.session.query(PerevalAdded).filter(PerevalAdded.id == pereval_id).first()

        if not pereval:
            raise HTTPException(status_code=404, detail='Перевал не найден')

        coords = db.session.query(Coords).filter(Coords.id == pereval.coord_id).first()
        user = pereval.user

        # Ответ в JSON-формате
        return {
            'id': pereval.id,
            'author': user.email,
            'beautytitle': pereval.beautytitle,
            'title': pereval.title,
            'other_titles': pereval.other_titles,
            'connect': pereval.connect,
            'add_time': pereval.add_time,
            'status': pereval.status,
            'coords': {
                'latitude': coords.latitude,
                'longitude': coords.longitude,
                'height': coords.height
            },
            'level': {
                'winter': pereval.winter,
                'summer': pereval.summer,
                'autumn': pereval.autumn,
                'spring': pereval.spring
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')


@app.patch('/submitData/{id}', summary='Редактирование перевала',
           description='Позволяет редактировать перевал, если его статус "new"',
           responses={200: {'description': 'Данные успешно обновлены'},
                      403: {'description': 'Редактирование невозможно'},
                      404: {'description': 'Перевал не найден'}})
async def update_pereval(id: int, data: SubmitData, db: Database = Depends(get_db)):
    """Редактирование информации о перевале со статусом new"""
    pereval = db.session.query(PerevalAdded).filter(PerevalAdded.id == id).first()

    if not pereval:
        return {'state': 0, 'message': 'Перевал не найден'}

    if pereval.status != 'new':
        return {'state': 0, 'message': 'Редактирование невозможно'}

    try:
        # Обновляем только разрешенные поля
        pereval.beautytitle = data.beautytitle
        pereval.title = data.title
        pereval.other_titles = '; '.join(data.other_titles)
        pereval.connect = data.connect
        pereval.add_time = data.add_time.isoformat()
        pereval.winter = data.winter
        pereval.summer = data.summer
        pereval.autumn = data.autumn
        pereval.spring = data.spring

        # Обновляем координаты
        coords = db.session.query(Coords).filter(Coords.id == pereval.coord_id).first()
        coords.latitude = data.latitude
        coords.longitude = data.longitude
        coords.height = data.height

        db.session.commit()
        return {'state': 1, 'message': 'Данные успешно обновлены'}

    except Exception as e:
        return {'state': 0, 'message': f'Ошибка при обновлении данных: {str(e)}'}


@app.get('/submitData/', summary='Просмотр перевалов пользователя по его email',
         description='Возвращает список перевалов, добавленных пользователем по его email',
responses={
             200: {
                 'description': 'Перевалы пользователя найдены',
                 'content': {
                     'application/json': {
                         'example': {
                             'email': 'user@example.com',
                             'perevals': [
                                 {
                                     'id': 1,
                                     'title': 'Перевал Дятлова',
                                     'beautytitle': 'Перевал на Урале',
                                     'status': 'new',
                                     'add_time': '2024-03-01T12:00:00Z'
                                 },
                                 {
                                     'id': 2,
                                     'title': 'Горный хребет',
                                     'beautytitle': 'Высокий перевал',
                                     'status': 'pending',
                                     'add_time': '2024-03-02T15:30:00Z'
                                 }
                             ]
                         }
                     }
                 }
             },
             404: {'description': 'Пользователь с таким email не найден'},
             500: {'description': 'Ошибка сервера'}
         })
async def get_perevals_by_email(user__email: str, db: Database = Depends(get_db)):
    """Просмотр всех перевалов, опубликованных пользователем с определенным email-ом"""
    user__email = user__email.strip()  # Удаление пробелов
    user = db.session.query(User).filter(User.email.ilike(user__email)).first()

    if not user:
        raise HTTPException(status_code=404, detail='Пользователь с таким email не найден')

    perevals = db.session.query(PerevalAdded).filter(PerevalAdded.user_id == user.id).all()

    return {'Перевалы пользователя': user__email, 'data': perevals}

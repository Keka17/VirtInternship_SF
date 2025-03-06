from datetime import datetime
import re

from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Field, conlist, field_validator, EmailStr
import pendulum

from database import Database, PerevalAdded, Coords, User


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
async def validation_exception_handler(exc):
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
    add_time: datetime = Field(default_factory=pendulum.now,
                               description='Дата и время добавления данных в UTC')
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
        iso_8601_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?$'

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

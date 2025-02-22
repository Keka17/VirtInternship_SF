from datetime import datetime

from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.params import Depends

from pydantic import BaseModel, Field, conlist, field_validator
import pendulum

from database import Database, PerevalAdded, Coords

app = FastAPI()

# Эндпоинт для проверки API
@app.get('/')
async def root():
    return {'message': 'API работает!'}


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

    @field_validator('add_time', mode='before')
    def parse_add_time(cls, value):
        """Валидатор для обработки формата даты (ISO 8601)"""
        if isinstance(value, str):
            try:
                return pendulum.parse(value)  # Автоопределение формата (ISO 8601, RFC 3339)
            except pendulum.parsing.exceptions.ParserError:
                raise ValueError('add_time должен быть в формате ISO 8601 (YYYY-MM-DDTHH:MM:SSZ) или datetime объект')
        return value


def get_db():
    """Создание сесии БД для запроса и ее закрытие после использования"""
    db = Database()
    try:
        yield db  # Экземпляр db будет передан в функцию-обработчик запроса
    finally:
        db.close()  # Гарантированное закрытие сессии в любом случае


@app.post('/submitData')
async def submit_data(data: SubmitData, db: Database = Depends(get_db)):
    """Обработчик POST-запроса для добавления нового перевала"""
    try:
        pereval_id = db.add_pereval(
            beautytitle=data.beautytitle,
            title=data.title,
            other_titles='; '.join(data.other_titles),
            connect=data.connect,
            add_time=data.add_time.isoformat(),
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


@app.get('/submitData/{pereval_id}')
async def get_pereval(pereval_id: int, db: Database = Depends(get_db)):
    """Получение информации о перевале по id"""
    try:
        pereval = db.session.query(PerevalAdded).filter(PerevalAdded.id == pereval_id).first()

        if not pereval:
            raise HTTPException(status_code=404, detail='Перевал не найден')

        coords = db.session.query(Coords).filter(Coords.id == pereval.coord_id).first()

        # Ответ в JSON-формате
        return {
            'id': pereval.id,
            'beautytitle': pereval.beautytitle,
            'title': pereval.title,
            'other_titles': pereval.other_titles,
            'connect': pereval.connect,
            'add_time': pereval.add_time,
            'status': pereval.status,
            'coords': {
                "latitude": coords.latitude,
                "longitude": coords.longitude,
                "height": coords.height
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


@app.patch('/submitData/{id}')
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

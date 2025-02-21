from datetime import datetime

from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.params import Depends

from pydantic import BaseModel, Field, conlist, field_validator
import pendulum

from database import Database

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
            height=data.height
        )

        return {'status': 'success', 'pereval_id': pereval_id}  # JSON-ответ

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка сервера: {str(e)}')

from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field, conlist, field_validator
import pendulum


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
    add_time: datetime = Field(default_factory=datetime.datetime.now(datetime.timezone.utc),
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


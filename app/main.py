from fastapi import FastAPI

app = FastAPI()


# Эндпоинт для проверки работы API
@app.get('/')
async def root():
    return {'message': 'API успешном работает!'}

from fastapi import FastAPI

app = FastAPI()

# Эндпоинт для проверки API
@app.get('/')
async def root():
    return {'message': 'API работает!'}
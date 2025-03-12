from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_submit_data():
    """Тест на добавление нового перевала через API"""
    response = client.post('/submitData', json={
        'beautytitle': 'Перевал Лунного Света',
        'title': 'Лунный перевал',
        'other_titles': ['Серебряный перевал', 'Перевал Ночи'],
        'connect': '',
        'add_time': '2023-11-07T18:45:00Z',  # Можно закомментить, чтобы добавилось актуальное время
        'latitude': 47.8901,
        'longitude': 91.2345,
        'height': 3120,
        'winter': '1A',
        'summer': '1B',
        'autumn': '1A',
        'spring': '1B',
        'fam': 'Тестовый',
        'name': 'Тестим',
        'otc': 'Тестович',
        'phone': '12345678912',
        'email': 'testim@gmail.com'
    })

    assert response.status_code == 200
    data = response.json()
    assert 'pereval_id' in data  # Проверяем ключ 'pereval_id'
    print(f'ID нового перевала: {data['pereval_id']}')


def test_get_pereval():
    """Тест на получение данных о перевале"""
    pereval_id = 39
    response = client.get(f'/submitData/{pereval_id}')

    if response.status_code == 404:
        return 'Перевал с таким id не найден '

    print(response.json())  # Выведет подробности ошибки

    assert response.status_code == 200
    data = response.json()

    assert 'id' in data
    assert 'title' in data
    assert 'beautytitle' in data
    assert 'other_titles' in data
    assert 'author' in data
    assert 'connect' in data
    assert 'status' in data
    assert 'coords' in data
    assert 'level' in data

    print(f'Полученные данные: {data}')
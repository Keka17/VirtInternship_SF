import pytest
from database import Database, User


@pytest.fixture
def db():
    """Фикстура для создания и очистки базы после тестов"""
    db = Database()
    yield db
    db.close()


def test_add_pereval(db):
    """Тест на добавление перевала в БД"""

    # Данные автора
    fam = 'Петров'
    name = 'Петр'
    otc = 'Петрович'
    phone = '9999999990'
    email = 'petrov@example.com'

    # Проверяем, существует ли пользователь с таким email
    existing_user = db.session.query(User).filter(User.email == email).first()
    if existing_user:
        print(f'Пользователь с email {email} уже существует: ID {existing_user.id}')
    else:
        print(f'Пользователь с email {email} не найден, создаем нового.')

    # Получаем или создаем пользователя
    user_id = db.get_or_create_user(fam, name, otc, phone, email)

    # Добавляем перевал с указанием user_id
    new_id = db.add_pereval(
        beautytitle='Перевал Семи Ветров',
        title='Семиветровый перевал',
        other_titles=['Ветряной перевал', 'Перевал Стихий'],
        connect='Плохая связь',
        add_time='2024-12-08T14:30:45.123456',  # Можно закомментить, чтобы добавилось актуальное время
        latitude=48.1234,
        longitude=92.5678,
        height=2789,
        winter='3A',
        summer='2B',
        autumn='2A',
        spring='2B',
        user_id=user_id
    )

    assert new_id is not None
    print(f'Добавлен новый перевал: {new_id}')

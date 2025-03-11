# VirtInternship_SF

Этот проект работает на фреймворке FAST-API для хранения и обработки данных о перевалах. 

Функциональность:
- Проверка работоспособности API (GET/)
- Добавление нового перевала (POST /submitData)
- Редактирование перевала, если он в статусе `new` (PATCH /submitData/{id})
- Получение информации о перевале по ID (GET /submitData/{pereval_id})
- Получение списка перевалов, отправленных конкретным пользователем по его email-адресу (GET /submitData/?user_email=example@email.com)

Начало работы:

• Клонирование репозитория
git clone https://github.com/Keka17/VirtInternsip_SF.git
cd VirtInternsip_SF

• Создание и активация виртуального окружения
python -m venv venv
source venv/bin/activate  # для macOS/Linux
venv\Scripts\activate  # для Windows

• Установка зависимостей 
pip install -r requirements.txt

• Настройка БД

a) Создание базы данных

Убедитесь, что PostgreSQL установлен и запущен.
Создайте базу данных:
psql -U postgres -c "CREATE DATABASE pereval;"

b) Импорт данных из файла .sql
В репозитории находится файл pereval_db.sql, который содержит дамп базы данных. Чтобы импортировать данные, выполните команду:
psql -U postgres -d pereval -f pereval_db.sql
Если вы используете другую базу данных, измените параметры подключения в файле .env.

c) Настройка переменных окружения
Создайте файл .env в корневой папке проекта и добавьте в него данные для подключения к PostgreSQL:

DB_HOST = "localhost"
DB_PORT = "5432"
DB_LOGIN = "postgres"
DB_PASS = "yourpassword"
DB_NAME = "pereval" 

• Запуск сервера 
uvicorn main:app --reload

• Проверка работы
Перейдите по ссылке http://127.0.0.1:8000/swagger для отправки тестовых запросов

Основные установленные зависимости: 
fastapi — фреймворк для создания API
uvicorn — сервер для запуска FastAPI
sqlalchemy — ORM для работы с базой данных
psycopg2 — драйвер для подключения к PostgreSQL
python-dotenv — для работы с переменными окружения

Для связи: vihalfblood@gmail.com

upd: Работоспособность можно проверить тестами, для этого в терминале введите 
cd app
PYTHONPATH=$(pwd) pytest -v tests/test_database.py или PYTHONPATH=$(pwd) pytest -v tests/test_api.py

upd: Документация с помощью Swagger UI
API предоставляет документацию в двух форматах:
Swagger UI: Доступна по адресу /swagger
Redoc: Доступна по адресу /api-docs

API возвращает понятные ошибки:
422 Unprocessable Entity — Ошибка валидации запроса (неверный формат данных)
404 Not Found — Перевал/пользователь не найден
403 Forbidden — Редактирование невозможно
500 Internal Server Error — Ошибка сервера

upd: Деплой на Render 
Изменения в коде: Объединила файлы database.py и main.py для устранения конфликта ModuleNotFound (ветка render).
Для проверки работы API перейдите по одной из следующих ссылок: https://virtinternship-sf-6wau.onrender.com/swagger или  https://virtinternship-sf-6wau.onrender.com/api-docs
Сервер подключен к базе данных в Supabase.
Работоспособность API можно проверить для перевалов с id от 1, 3, 4, 5, 6.


# VirtInternship_SF #

Этот проект работает на фреймворке ___FAST-API___ для хранения и обработки данных о перевалах. 

__Функциональность__:
- Проверка работоспособности API (GET/)
- Добавление нового перевала (POST /submitData)
- Редактирование перевала, если он в статусе `new` (PATCH /submitData/{id})
- Получение информации о перевале по ID (GET /submitData/{pereval_id})
- Получение списка перевалов, отправленных конкретным пользователем по его email-адресу (GET /submitData/?user_email=example@email.com)


__Начало работы__:
1. Клонирование репозитория\
  git clone https://github.com/Keka17/VirtInternsip_SF.git<br>
  cd VirtInternsip_SF
2. Создание и активация виртуального окружения\
  python -m venv venv\
  source venv/bin/activate  # для macOS/Linux \
  venv\Scripts\activate  # для Windows
3. Установка зависимостей\
pip install -r requirements.txt


__Настройка БД__
1. Убедитесь, что _PostgreSQL_ установлен и запущен.\
Создайте базу данных:
psql -U postgres -c "CREATE DATABASE pereval;"
2. Импорт данных из файла .sql:\
В репозитории находится файл pereval_dump.sql, который содержит дамп базы данных. Чтобы импортировать данные, выполните команду:\
psql -U postgres -d pereval -f pereval_dump.sql\
Если вы используете другую базу данных, измените параметры подключения в файле .env.\
Альтернативный способ с использованием pgAdmin4: Tools -> Query Tool-> в открывшемся окне ввести содержимое файла pereval_dump.sql.
3. Настройка переменных окружения:\
Создайте файл .env в корневой папке проекта и добавьте в него данные для подключения к _PostgreSQL_:\
DB_HOST = "localhost"\
DB_PORT = "5432"\
DB_LOGIN = "postgres"\
DB_PASS = "yourpassword"\
DB_NAME = "pereval"
4. Запуск сервера:\
uvicorn main:app --reload


__Проверка работы__:\
Перейдите по ссылке http://127.0.0.1:8000/swagger для отправки тестовых запросов.


__Основные установленные зависимости__:\
_fastapi_ — фреймворк для создания API\
_uvicorn_ — сервер для запуска FastAPI\
_sqlalchemy_ — ORM для работы с базой данных\
_psycopg2_ — драйвер для подключения к PostgreSQL\
_python-dotenv_ — для работы с переменными окружения


Для связи: _vihalfblood@gmail.com_


upd: Работоспособность можно проверить тестами, для этого в терминале введите<br>
cd app\
PYTHONPATH=$(pwd) pytest -v tests/test_database.py или PYTHONPATH=$(pwd) pytest -v<br>
tests/test_api.py


upd: __Документация с помощью Swagger UI__\
API предоставляет документацию в двух форматах:\
_Swagger UI_: Доступна по адресу /swagger\
_Redoc_: Доступна по адресу /api-docs

API возвращает понятные ошибки:\
__422 Unprocessable Entity__ — Ошибка валидации запроса (неверный формат данных)\
__404 Not Found__ — Перевал/пользователь не найден\
__403 Forbidden__ — Редактирование невозможно\
__500 Internal Server Error__ — Ошибка сервера




#### Неактуально #
upd: __Деплой на Render__\
Изменения в коде:\
Объединила файлы database.py и main.py для устранения конфликта ModuleNotFound (ветка render).
Для проверки работы API перейдите по одной из следующих ссылок: https://virtinternship-sf-6wau.onrender.com/swagger или  https://virtinternship-sf-6wau.onrender.com/api-docs
Сервер подключен к базе данных в Supabase.
Работоспособность API можно проверить для перевалов с id от 1, 3, 4, 5, 6.


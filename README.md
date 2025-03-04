# VirtInternship_SF

Этот проект работает на фреймворке FAST-API для хранения и обработки данных о перевалах. 

Функциональность:
- Добавление нового перевала
- Редактирование перевала (если он в статусе `new`)
- Получение информации о перевале по ID
- Получение списка перевалов, отправленных конкретным пользователем (по его email-адресу)

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
Перейдите по ссылке http://127.0.0.1:8000/docs для доступа к документации Swagger UI.

Основные установленны зависимости: 
fastapi — фреймворк для создания API
uvicorn — сервер для запуска FastAPI
sqlalchemy — ORM для работы с базой данных
psycopg2 — драйвер для подключения к PostgreSQL
python-dotenv — для работы с переменными окружения

Для связи: vihalfblood@gmail.com

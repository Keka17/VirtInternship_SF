from database import Database

db = Database()

# Добавим новый перевал
new_id = db.add_pereval('Мглистые горы', 'Тестовая запись',
                        'Еще одна запись', 'Связь',
                        '2025-02-20', 42.1234, 74.5678, 3000)

print(f'Добавлен новый перевал  {new_id}')

db.close()
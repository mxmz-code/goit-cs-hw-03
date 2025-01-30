import psycopg2
from faker import Faker
import random

# Підключення до бази даних
conn = psycopg2.connect(
    dbname="task_manager",
    user="your_username",
    password="your_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Ініціалізація Faker
faker = Faker()

# Додавання випадкових користувачів
num_users = 15  # Кількість користувачів
users = []
for _ in range(num_users):
    fullname = faker.name()
    email = faker.unique.email()
    cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id", (fullname, email))
    user_id = cursor.fetchone()[0]
    users.append(user_id)

# Отримання доступних статусів завдань
cursor.execute("SELECT id FROM status")
status_ids = [row[0] for row in cursor.fetchall()]

# Додавання випадкових завдань
num_tasks = 40  # Кількість завдань
for _ in range(num_tasks):
    title = faker.sentence(nb_words=6)
    description = faker.text()
    status_id = random.choice(status_ids)
    user_id = random.choice(users)
    cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                   (title, description, status_id, user_id))

# Виконання необхідних SQL-запитів

# 1. Отримати всі завдання певного користувача
cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (users[0],))
print("Завдання користувача:", cursor.fetchall())

# 2. Вибрати завдання за певним статусом
cursor.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new')")
print("Завдання зі статусом 'new':", cursor.fetchall())

# 3. Оновити статус конкретного завдання
cursor.execute("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = %s", (1,))

# 4. Отримати список користувачів, які не мають жодного завдання
cursor.execute("SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)")
print("Користувачі без завдань:", cursor.fetchall())

# 5. Додати нове завдання для конкретного користувача
cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES ('New Task', 'Description', 1, %s)", (users[0],))

# 6. Отримати всі завдання, які ще не завершено
cursor.execute("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed')")
print("Незавершені завдання:", cursor.fetchall())

# 7. Видалити конкретне завдання
cursor.execute("DELETE FROM tasks WHERE id = %s", (1,))

# 8. Знайти користувачів з певною електронною поштою
cursor.execute("SELECT * FROM users WHERE email LIKE '%@example.com'")
print("Користувачі з доменом @example.com:", cursor.fetchall())

# 9. Оновити ім'я користувача
cursor.execute("UPDATE users SET fullname = 'Updated Name' WHERE id = %s", (users[0],))

# 10. Отримати кількість завдань для кожного статусу
cursor.execute("SELECT status_id, COUNT(*) FROM tasks GROUP BY status_id")
print("Кількість завдань за статусами:", cursor.fetchall())

# 11. Отримати завдання для користувачів з певною доменною частиною email
cursor.execute("SELECT tasks.* FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.email LIKE '%@example.com'")
print("Завдання для користувачів з доменом @example.com:", cursor.fetchall())

# 12. Отримати список завдань без опису
cursor.execute("SELECT * FROM tasks WHERE description IS NULL OR description = ''")
print("Завдання без опису:", cursor.fetchall())

# 13. Вибрати користувачів та їхні завдання у статусі 'in progress'
cursor.execute("SELECT users.fullname, tasks.title FROM users JOIN tasks ON users.id = tasks.user_id JOIN status ON tasks.status_id = status.id WHERE status.name = 'in progress'")
print("Користувачі та їхні завдання у статусі 'in progress':", cursor.fetchall())

# 14. Отримати користувачів та кількість їхніх завдань
cursor.execute("SELECT users.fullname, COUNT(tasks.id) FROM users LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY users.fullname")
print("Кількість завдань для кожного користувача:", cursor.fetchall())

# Збереження змін та закриття з'єднання
conn.commit()
cursor.close()
conn.close()

print("База даних успішно заповнена випадковими даними та перевірена SQL-запитами!")

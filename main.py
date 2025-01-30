from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["cats_db"]
    cats_collection = db["cats"]
    print("Підключено до бази даних.")
except Exception as e:
    print(f"Помилка при підключенні до MongoDB: {e}")

# Функція для виведення всіх записів
def get_all_cats():
    try:
        for cat in cats_collection.find():
            print(cat)
    except Exception as e:
        print(f"Помилка при отриманні всіх котів: {e}")

# Функція для отримання кота за ім'ям
def get_cat_by_name(name):
    try:
        cat = cats_collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("Кіт не знайдений")
    except Exception as e:
        print(f"Помилка при отриманні кота за ім'ям: {e}")

# Функція для оновлення віку кота
def update_cat_age(name, new_age):
    try:
        result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print("Оновлено")
        else:
            print("Кота не знайдено")
    except Exception as e:
        print(f"Помилка при оновленні віку кота: {e}")

# Функція для додавання характеристики коту
def add_feature(name, feature):
    try:
        result = cats_collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.modified_count > 0:
            print("Оновлено")
        else:
            print("Кота не знайдено")
    except Exception as e:
        print(f"Помилка при додаванні характеристики коту: {e}")

# Функція для видалення кота за ім'ям
def delete_cat_by_name(name):
    try:
        result = cats_collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print("Видалено")
        else:
            print("Кота не знайдено")
    except Exception as e:
        print(f"Помилка при видаленні кота: {e}")

# Функція для видалення всіх записів
def delete_all_cats():
    try:
        result = cats_collection.delete_many({})
        print(f"Видалено {result.deleted_count} записів")
    except Exception as e:
        print(f"Помилка при видаленні всіх записів: {e}")

if __name__ == "__main__":
    # Тестові виклики функцій
    get_all_cats()
    get_cat_by_name("barsik")
    update_cat_age("barsik", 5)
    add_feature("barsik", "любить спати на сонці")
    delete_cat_by_name("barsik")
    delete_all_cats()

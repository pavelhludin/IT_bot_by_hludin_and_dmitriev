import csv

def save_user(user_id: int, name: str, email: str):
    """
    Сохраняет данные пользователя в CSV-файл.
    """
    with open("data/users.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([user_id, name, email])

def is_user_registered(user_id: int) -> bool:
    """
    Проверяет, зарегистрирован ли пользователь.
    """
    try:
        with open("data/users.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if row and int(row[0]) == user_id:
                    return True
    except FileNotFoundError:
        return False
    return False

def log_user_action(user_id: int, action: str):
    """
    Логирует действия пользователя в CSV-файл.
    """
    with open("data/user_actions.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([user_id, action])

def get_user_data(user_id: int):
    """
    Получает данные пользователя из CSV-файла.
    """
    try:
        with open("data/users.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if row and int(row[0]) == user_id:
                    return row[1], row[2]
    except FileNotFoundError:
        return None
    return None

def update_user_data(user_id: int, name: str = None, email: str = None):
    """
    Обновляет данные пользователя в CSV-файле.
    """
    users = []
    try:
        with open("data/users.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            for row in reader:
                if row and int(row[0]) == user_id:
                    if name:
                        row[1] = name
                    if email:
                        row[2] = email
                users.append(row)
    except FileNotFoundError:
        return

    with open("data/users.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(users)
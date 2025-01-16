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
import json
import os

FILENAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            tasks = json.load(f)
            return tasks
    except json.JSONDecodeError:
        return []


def save_tasks(tasks):

    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def view_tasks(tasks):

    if not tasks:
        print("Список задач пуст.")
    else:
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task['title']} — [{task['priority']}]")


def add_task(tasks):

    title = input("Введите название задачи: \n")
    priority = int(input("Введите приоритет (1 - Низкий/2 - Средний/3 - Высокий): \n"))

    priority_type = ["низкий", "средний","высокий"]
    
    task = {"title": title, "priority": priority_type[priority]}
    tasks.append(task)
    save_tasks(tasks)
    print("Задача добавлена\n")


def delete_task(tasks):

    try:
        number = input("Введите номер задачи\n")
        num = int(number)
        var = 1 <= num <= len(tasks)
        tasks.pop(num - 1)
        save_tasks(tasks)
        print("Задача удалена\n")

    except ValueError:
        print("Введено некорректное число\n")


def main():
    print("Добро пожаловать в менеджер задач!")
    tasks = load_tasks()

    while True:
        print("\nМеню:")
        print("1 — Просмотреть задачи")
        print("2 — Добавить задачу")
        print("3 — Удалить задачу")
        print("0 — Выход")

        choice = input("Выберите пункт меню: \n")

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "0":
            print("Выход из программы.\n")
            break
        else:
            print("Ошибка: такого пункта меню нет. Попробуйте снова.\n")


if __name__ == "__main__":
    main()

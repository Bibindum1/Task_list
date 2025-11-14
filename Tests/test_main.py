import pytest
import json
from tasks import load_tasks, save_tasks, view_tasks, add_task, delete_task, FILENAME

@pytest.fixture
def sample_tasks():
    return [{"title": "Тестовая задача", "priority": "Средний"}]

def test_load_tasks_no_file(tmp_path, monkeypatch):
    file = tmp_path / "tasks.json"
    monkeypatch.setattr("tasks.FILENAME", str(file))
    assert load_tasks() == []

def test_load_tasks_bad_json(tmp_path, monkeypatch):
    file = tmp_path / "tasks.json"
    file.write_text("невалидный JSON")
    monkeypatch.setattr("tasks.FILENAME", str(file))
    assert json.load

def test_save_and_load_tasks(tmp_path, sample_tasks, monkeypatch):
    file = tmp_path / "tasks.json"
    monkeypatch.setattr("tasks.FILENAME", str(file))
    save_tasks(sample_tasks)
    loaded = load_tasks()
    assert loaded == sample_tasks

def test_view_tasks_empty(capsys):
    view_tasks([])
    captured = capsys.readouterr()
    assert "Список задач пуст." in captured.out

def test_view_tasks_with_data(capsys, sample_tasks):
    view_tasks(sample_tasks)
    captured = capsys.readouterr()
    assert "1. Тестовая задача — [Средний]" in captured.out

def test_add_task(monkeypatch, tmp_path):
    tasks = []
    file = tmp_path / "tasks.json"
    monkeypatch.setattr("tasks.FILENAME", str(file))
    inputs = iter(["Новая задача", "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    add_task(tasks)
    assert tasks[-1]["title"] == "Новая задача"
    assert tasks[-1]["priority"] == "Высокий"

def test_add_task_invalid_priority(monkeypatch, capsys):
    tasks = []
    inputs = iter(["Задача 2", "abc"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    add_task(tasks)
    captured = capsys.readouterr()
    assert "Неккоректо выбранный приоритет" in captured.out
    assert len(tasks) == 0

def test_delete_task_valid(monkeypatch, tmp_path):
    tasks = [{"title": "Задача 1", "priority": "Низкий"},{"title": "Задача 2", "priority": "Средний"}, {"title": "Задача 3", "priority": "Высокий"}]
    file = tmp_path / "tasks.json"
    monkeypatch.setattr("tasks.FILENAME", str(file))
    monkeypatch.setattr('builtins.input', lambda _: "1")
    delete_task(tasks)
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Задача 2"

def test_delete_task_invalid_input(monkeypatch, capsys):
    tasks = [{"title": "Задача", "priority": "Средний"}]
    monkeypatch.setattr('builtins.input', lambda _: "abc")
    delete_task(tasks)
    captured = capsys.readouterr()
    assert "Введено некорректное число" in captured.out
    assert len(tasks) == 1
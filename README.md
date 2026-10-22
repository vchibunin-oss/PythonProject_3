# PythonProject_3 — Aircraft Tracker

## Описание проекта

Aircraft Tracker — учебный Python-проект для получения информации о воздушных судах через внешние API и сохранения данных в PostgreSQL.

Проект позволяет:
- получать координаты стран через Nominatim;
- получать данные о воздушных судах через OpenSky;
- сохранять информацию в базе данных PostgreSQL;
- просматривать количество воздушных судов по странам;
- рассчитывать среднюю скорость;
- находить воздушные суда, движущиеся быстрее средней скорости;
- искать воздушные суда по части позывного.

**Важно:** данные собираются в радиусе 300 км от координат, возвращаемых для каждой страны. Это не является полным учётом воздушного пространства страны.

## Технологии

- Python
- PostgreSQL
- Requests
- Psycopg2
- python-dotenv
- Pytest
- pytest-cov
- Black
- Flake8
- isort

## Структура проекта

```text
PythonProject_3/
├── src/
│   ├── __init__.py
│   ├── api.py
│   ├── database.py
│   ├── loader.py
│   └── db_manager.py
├── tests/
│   ├── test_api.py
│   ├── test_database.py
│   ├── test_db_manager.py
│   └── test_loader.py
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Установка и запуск

### 1. Подготовка окружения

Создайте виртуальное окружение:

```bash
python -m venv .venv
```

Активируйте его на macOS:

```bash
source .venv/bin/activate
```

### 2. Установка зависимостей

```bash
python -m pip install -r requirements.txt
```

### 3. Настройка базы данных

Установите PostgreSQL и создайте базу данных `aircraft_tracker`.

Создайте файл `.env` в корне проекта и укажите параметры подключения:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=aircraft_tracker
DB_USER=postgres
DB_PASSWORD=your_password
```

Замените `your_password` на пароль пользователя PostgreSQL. Не публикуйте `.env` и не добавляйте реальные пароли в репозиторий.

### 4. Запуск программы

Из корневой папки проекта выполните:

```bash
python main.py
```

Программа создаст таблицы, загрузит координаты стран и попытается получить данные о воздушных судах.

Для работы необходим доступ к интернету, работающий PostgreSQL и доступность внешних API.

## Запуск тестов

Запуск всех тестов:

```bash
python -m pytest -v
```

Проверка покрытия:

```bash
python -m pytest --
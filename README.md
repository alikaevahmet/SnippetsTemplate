# Snippets

## Инструкция по развертыванию проекта
1. `python3 -m venv snippets_venv`

2. `source snippets_venv/bin/activate`

3. `pip install -r requirements.txt`

4. `python manage.py migrate`

5. `python manage.py runserver`


## Запуск `ipython` в контексте `django` приложений
```
python manage.py shell_plus --ipython
```

## Выгрузка и загрузка данных при работе с БД
### Выгрузить данные из БД
```
python manage.py dumpdata MainApp --indent 4 > MainApp/fixtures/save_all.json
```
### Загрузить данные в БД
```
python manage.py loaddata MainApp/fixtures/save_all.json
```

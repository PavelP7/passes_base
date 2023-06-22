<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/PavelP7/passes_base">
    <img src="PassesBase/media/images/logo.jpg" alt="Logo" width="300" height="150">
  </a>

<a name="readme-top"></a>
<h3 align="center">База данных перевалов </h3>

  <p align="center">
    Backend-часть сервиса добавления информации о перевале туристами.
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
## Содержание
1. [О проекте](#О-проекте)
   * [Стек](#Стек)
1. [Начало работы](#Начало-работы)
   * [Установка](#Установка)
1. [Как пользоваться](#Как-пользоваться)
   * [Запросы по REST API](#Запросы-по-REST-API)
   * [Swagger](#Swagger)
   * [Unittest](#Unit-test)
1. [Загрузка с хостинга](#Загрузка-с-хостинга)

<!-- ABOUT THE PROJECT -->
## О проекте

Проект представляет собой сервис по добавлению информации о перевале туристами через мобильное приложение. Взаимодействие с frontend-частью осуществляется при помощи REST API.

Проект предоставляет следующие возможности:
* Добавление информации о перевале
* Редактирование уже имеющейся информации
* Получение информации по идентификатору перевала
* Получение информации о всех добавленных перевалах туристом по его email.

<p align="right">(<a href="#readme-top">наверх</a>)</p>



### Стек

* [![Python][Python.com]][Python-url]
* [![Django][Django.com]][Django-url]
* [![Swagger][Swagger.com]][Swagger-url]
* [![PostgreSQL][Postgres.com]][Postgres-url]
* [![Unittest][Unittest.com]][Unittest-url]

<p align="right">(<a href="#readme-top">наверх</a>)</p>



<!-- GETTING STARTED -->
## Начало работы

Перед установкой и запуском проекта Вам необходимо установить **git**.

### Установка

Выполните следующие шаги для корректной установки проекта.
1. Клонируйте репозиторий
```sh
git clone https://github.com/PavelP7/passes_base.git
```
2. Установите требуемую версию **python** из файла *pythonversion.txt*
3. Перейдите в каталог *passes_base*, создайте и активируйте виртуальную среду
```sh
cd passes_base
python -m venv venv
venv\scripts\activate
```
4. Установите необходимые модули
```sh
pip install -r requirements.txt
cd PassesBase
```
5. Создайте файл *.env* с переменными среды из файла *.env.example* в этой же директории

<p align="right">(<a href="#readme-top">наверх</a>)</p>

<!-- USAGE EXAMPLES -->
## Как пользоваться
Запустите сервер при помощи команды ```python manage.py runserver```

### Запросы по REST API
1. Для добавления информации о перевале используйте метод POST
  ```http://127.0.0.1:8000/passes/```   
  с содержимым в формате *json*, как представлено ниже
  ```
  {
  "beauty_title": "пер. ",
  "title": "Название",
  "other_titles": "Название",
  "connect": "",
  "add_time": "2021-09-22 13:18:13",
  
  "user": {"email": "qwerty@mail.ru",
           "fam": "Имя",
           "name": "Фамилия",
           "otc": "Отчество",
           "phone": "+7 555 55 55"},
        
  "coords":{
  "latitude": "45.3842",
  "longitude": "7.1525",
  "height": "1200"},
  
  "level":{"winter": "",
  "summer": "1А",
  "autumn": "1А",
  "spring": ""},
  
  "images": [{"data": "", "title":"Название1"}, {"data": "", "title":"Название2"}]
  }
  ```
Данные изображений предоставляются в текстовом виде. Для конвертации изображения в текст можно воспользоваться сервисом [base64.guru](https://base64.guru/converter/encode).

Результаты метода в формате JSON

* status — код HTTP, целое число: 500 — ошибка при выполнении операции;
  400 — некорректные поля в запросе; 200 — успех
* message — строка: причина ошибки (если она была); null, если отправлено успешно. Если отправка успешна, дополнительно возвращается id созданной записи (идентификатор записи перевала).

Примеры:
```json
{"status": 500, "message": "Ошибка подключения к базе данных","id": null}
{"status": 400, "message": "Bad Request","id": null}
{"status": 200, "message": null, "id": 42}
```
2. Для получения информации о перевале по *id* используйте метод GET
 ```http://127.0.0.1:8000/passes/<id>``` 
 
 Результаты метода в формате JSON

* status — код HTTP, целое число: 500 — ошибка при выполнении операции;
  200 — успех
* message — строка: причина ошибки (если она была). Если запрос корректен, возвращаются данные о записи в БД в формате *json*.

Примеры:
```json
{"status": 500, "message": "Ошибка подключения к базе данных","id": null}
{"data": {<данные о записи>}}
```
3. Для получения информации о перевалах, добавленных конкретным пользователем, используйте метод GET с указанием *email* пользователя
 ```http://127.0.0.1:8000/passes/?user_email=qwerty@mail.ru``` 
 
 Результаты метода в формате JSON

* status — код HTTP, целое число: 500 — ошибка при выполнении операции;
  200 — успех
* message — строка: причина ошибки (если она была). Если запрос корректен, возвращаются данные о перевалах в формате *json*.

Примеры:
```json
{"status": 500, "message": "Ошибка подключения к базе данных","id": null}
{"data": {"pereval": {<данные о записи>}}}
```
4. Для обновления информации о перевалах, используйте метод PATCH
 ```http://127.0.0.1:8000/passes/<id>/``` 
 
 Результаты метода в формате JSON

* status — код HTTP, целое число: 500 — ошибка при выполнении операции;
  400 — некорректные поля в запросе; 200 — успех
* state — целое число: 1 — запись в БД успешно отредактирована; 0 — ошибка 
* message — строка: причина ошибки (если она была); null, если обновление успешно.

Примеры:
```json
{"state": 0, "message": "Некорректные данные запроса"}
{"state": 0, "message": "Обновление несуществующей записи"}
{"state": 0, "message": "Ошибка подключения к базе данных"}
{"state": 1, "message": null}
```
<p align="right">(<a href="#readme-top">наверх</a>)</p>

### Swagger

Для демонстрации и тестирования сервиса предоставлена возможность формирования запросов через Swagger. Для запуска введите в браузере
 ```http://127.0.0.1:8000/swagger-ui/```.
 
 Схема формирования запросов также описана в файле *openapi-schema-passes.yml*.
<p align="right">(<a href="#readme-top">наверх</a>)</p>

### Unittest

Проект содержит набор тестов для проверки корректности вносимых изменений в модели *test_models.py* и в обработку запросов по REST API *test_rest_api.py* .

Для запуска всех тестов введите ```python manage.py test```.

Для запуска определенного набора тестов введите  
```python manage.py test --pattern="test_<название>.py"```.

<p align="right">(<a href="#readme-top">наверх</a>)</p>

## Загрузка с хостинга
Проект опубликован на сервисе *Yandex Cloud*. Для загрузки проекта с хостинга можно воспользоваться следующими командами:
* получить список объектов бакета
```sh
https://storage.yandexcloud.net/fstr-pereval-db?list-type=2&encoding-type=url&start-after=
```
* получить объект из бакета ({key} - наименование объекта)
```sh
https://storage.yandexcloud.net/fstr-pereval-db/{key}
```
<p align="right">(<a href="#readme-top">наверх</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Swagger.com]: https://img.shields.io/badge/swagger-white?style=for-the-badge&logo=laravel&logoColor=green
[Swagger-url]: https://swagger.io
[Django.com]: https://img.shields.io/badge/Django-white?style=for-the-badge&logo=django&logoColor=red
[Django-url]: https://github.com/django
[Python.com]: https://img.shields.io/badge/python-white?style=for-the-badge&logo=python&logoColor=blue
[Python-url]: https://python.org 
[Unittest.com]: https://img.shields.io/badge/Unittest-white?style=for-the-badge&logo=test&logoColor=red
[Unittest-url]: https://docs.djangoproject.com/en/2.1/topics/testing
[Postgres.com]: https://img.shields.io/badge/PostgreSQL-white?style=for-the-badge&logo=postgresql&logoColor=blue
[Postgres-url]: https://www.postgresql.org
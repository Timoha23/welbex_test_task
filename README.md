# WelbeX
## Описание
___
Данный сервис предоставляет поиск ближайших автомобилей для перевозки грузов. Вы можете добавлять грузы, отслеживать сколько автомобилей рядом с грузом (подходят по грузоподъемности и в пределах обозначенного расстояния (в милях)), для конкретного груза отслеживать точное расстояние до каждого автомобиля, обновлять информацию о грузах и автомобилях, удалять грузы. Так же локация каждого автомобиля автоматически обновляется* каждые 3 минуты.

<i>* - на случайную</i>
<details>
<summary>ТЗ проекта ↓</summary>

# **Тестовое задание web-программист Python** (Middle)

### #API: Сервис поиска ближайших машин для перевозки грузов.

<aside>
🔥 Необходимо разработать REST API сервиc для поиска ближайших машин к грузам.

</aside>

◼Стек и требования:

- **Python** (Django Rest Framework / FastAPI) на выбор.
- **DB** - Стандартный PostgreSQL.
- Приложение должно запускаться в docker-compose без дополнительных доработок.
- Порт - 8000.
- БД по умолчанию должна быть заполнена 20 машинами.
- Груз обязательно должен содержать следующие характеристики:
    - локация pick-up;
    - локация delivery;
    - вес (1-1000);
    - описание.
- Машина обязательно должна в себя включать следующие характеристики:
    - уникальный номер (цифра от 1000 до 9999 + случайная заглавная буква английского алфавита в конце, пример: "1234A", "2534B", "9999Z")
    - текущая локация;
    - грузоподъемность (1-1000).
- Локация должна содержать в себе следующие характеристики:
    - город;
    - штат;
    - почтовый индекс (zip);
    - широта;
    - долгота.

> *Список уникальных локаций представлен в прикрепленном csv файле "uszips.csv".*
> 
> 
> [uszips.csv](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/73ce520f-5205-47d4-8169-2266c628f6a7/uszips.csv)
> 
> *Необходимо осуществить выгрузку списка в базу данных Postgres при запуске приложения.*
> 
- При создании машин по умолчанию локация каждой машины заполняется случайным образом;
- Расчет и отображение расстояния осуществляется в милях;
- Расчет расстояния должен осуществляться с помощью библиотеки geopy. help(geopy.distance). Маршруты не учитывать, использовать расстояние от точки до точки.

<aside>
⭐ Задание разделено на 2 уровня сложности. Дедлайн по времени выполнения зависит от того, сколько уровней вы планируете выполнить.
**1 уровень** - 3 рабочих дня.
**2 уровень** - 4 рабочих дня.

</aside>

### ◼Уровень 1

Сервис должен поддерживать следующие базовые функции:

- Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду);
- Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль));
- Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза);
- Редактирование машины по ID (локация (определяется по введенному zip-коду));
- Редактирование груза по ID (вес, описание);
- Удаление груза по ID.

### ◼Уровень 2

Все что в уровне 1 + дополнительные функции:

- Фильтр списка грузов (вес, мили ближайших машин до грузов);
- Автоматическое обновление локаций всех машин раз в 3 минуты (локация меняется на другую случайную).

### ◼**Критерии оценки:**

- Адекватность архитектуры приложения;
- Оптимизация работы приложения.
</details>

## Используемые технологии
___
![AppVeyor](https://img.shields.io/badge/Python-3.10.6-green)
![AppVeyor](https://img.shields.io/badge/FastAPI-0.95.2-9cf)
![AppVeyor](https://img.shields.io/badge/Alembic-1.11.1-9cf)
![AppVeyor](https://img.shields.io/badge/SQLAlchemy-2.0.15-9cf)
![AppVeyor](https://img.shields.io/badge/Rocketry-2.5.1-9cf)
![AppVeyor](https://img.shields.io/badge/GeoPy-2.3.0-9cf)

![AppVeyor](https://img.shields.io/badge/Docker-23.0.5-green)
![AppVeyor](https://img.shields.io/badge/docker--compose-1.29.2-9cf)

![AppVeyor](https://img.shields.io/badge/Postgres-15.0-green)

## Модели
___

![imageup.ru](https://imageup.ru/img18/4357604/my-first-board-1.jpg)

## Запуск
___
###  Локально

1. Клонируем репозиторий:
   ```bash
   git clone https://github.com/Timoha23/welbex_test_task.git
   ```

2. Создаем .env файл и заполняем в соответствии с примером (.env.example).
3. Создаем и активируем виртуальное окружение:
   ```bash
    python -m venv venv
   ```
   ```bash
   source venv/Scripts/activate
   ```
4. Устанавливаем зависимости:
    ```bash
    pip install -r -requirements.txt
    ```
5. Накатываем миграции:
   ```bash
   python alembic upgrade head
   ```
6. Заполняем базу данных локациями:
   ```bash
   python app/fillers/fill_locations.py
   ```
7. Заполняем базу данных автомобилями:
   ```bash
   python app/fillers/fill_cars.py
   ```
8. Запускаем приложение:
   ```bash
   python app/main.py
   ```
###  Докер
1. Клонируем репозиторий:
   ```bash
   git clone https://github.com/Timoha23/welbex_test_task.git
   ```

2. Создаем .env файл и заполняем в соответствии с примером (.env.example).
3. Поднимаем контейнеры:
   ```bash
   docker-compose up -d --build
   ```

## Примеры запросов
___
1. Добавить груз
   * Endpoint: **host:port/cargo/**
   * Method: **POST**
   * Body: 
      ```json
      {
         "pick_up": "00601",
         "delivery": "00601",
         "weight": 999,
         "description": "description"
      }   
      ```
   * Response: 
      ```json
      {
        "id": "c0927a67-5dba-48d0-b6a2-fa98c8fe94d5",
        "pick_up": {
          "zip_code": "00601",
          "city": "Adjuntas",
          "state": "Puerto Rico",
          "longitude": -66.75266,
          "latitude": 18.18027,
          "created_date": "2023-05-30T07:08:35.911803"
        },
        "delivery": {
          "zip_code": "00601",
          "city": "Adjuntas",
          "state": "Puerto Rico",
          "longitude": -66.75266,
          "latitude": 18.18027,
          "created_date": "2023-05-30T07:08:35.911803"
        },
        "weight": 999,
        "description": "description",
        "created_date": "2023-05-30T07:52:50.899867"
      }
      ```
   * Postman
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][1]][1]
      
     [1]: https://imageup.ru/img290/4357655/welbex_create_cargo.jpg
     </details>

2. Получение всех грузов
   * Endpoint: **host:port/cargos/**
   * Method: **GET**
   * Params:
      * Query
      ```json
      {
        "max_car_distance": "1000",
        "weight__lte": "1000",
        "weight__gte": "1"
      }
      ```
   * Response: 
      ```json
      [
        {
          "id": "c0927a67-5dba-48d0-b6a2-fa98c8fe94d5",
          "pick_up": {
            "zip_code": "00601",
            "city": "Adjuntas",
            "state": "Puerto Rico",
            "longitude": -66.75266,
            "latitude": 18.18027,
            "created_date": "2023-05-30T07:08:35.911803"
          },
          "delivery": {
            "zip_code": "00601",
            "city": "Adjuntas",
            "state": "Puerto Rico",
            "longitude": -66.75266,
            "latitude": 18.18027,
            "created_date": "2023-05-30T07:08:35.911803"
          },
          "weight": 999,
          "description": "description",
          "created_date": "2023-05-30T07:52:50.899867"
        },
      ...
      ]
      ```
   * Postman
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][2]][2]
      
     [2]: https://imageup.ru/img251/4357656/welbex_get_cargos.jpg
     
     </details> 

3. Получение груза по ID
   * Endpoint: **host:port/cargo/{id}**
   * Method: **GET**
   * Params:
     * Path:
      ```json
      {
        "id": "7f15dd14-6893-4962-8192-1d6c2fa7e738"
      }
      ```
   * Response: 
      ```json
      {
        "id": "7f15dd14-6893-4962-8192-1d6c2fa7e738",
        "pick_up": {
          "zip_code": "00601",
          "city": "Adjuntas",
          "state": "Puerto Rico",
          "longitude": -66.75266,
          "latitude": 18.18027,
          "created_date": "2023-05-30T07:08:35.911803"
        },
        "delivery": {
          "zip_code": "00602",
          "city": "Aguada",
          "state": "Puerto Rico",
          "longitude": -67.17541,
          "latitude": 18.36075,
          "created_date": "2023-05-30T07:08:35.911803"
        },
        "weight": 100,
        "description": "string",
        "created_date": "2023-05-30T07:39:23.573880",
        "cars": [
          {
            "car_number": "7129S",
            "car_distance": 1996.4832892863594
          },
          ...
        ]
      }
      ```
   * Postman 
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][3]][3]
      
     [3]: https://imageup.ru/img56/4357658/welbex_get_cargo.jpg
     </details>
4. Обновление локации автомобиля
   * Endpoint: **host:port/car/{id}**
   * Method: **PATCH**
   * Params:
     * Path 
      ```json
      {
        "id": "2782X"
      }
      ```
   * Body: 
      ```json
      {
        "zip_code": "00601"
      }   
      ```
   * Response: 
      ```json
      {
        "id": "2782X",
        "location": {
          "zip_code": "00601",
          "city": "Adjuntas",
          "state": "Puerto Rico",
          "longitude": -66.75266,
          "latitude": 18.18027,
          "created_date": "2023-05-30T07:08:35.911803"
        },
        "load_capacity": 747,
        "created_date": "2023-05-30T07:38:49.094876"
      }
      ```
   * Postman 
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][4]][4]
      
     [4]: https://imageup.ru/img88/4357659/welbex_update_car.jpg
     </details>
5. Обновление информации о грузе
   * Endpoint: **host:port/cargo/{id}**
   * Method: **PATCH**
   * Params:
     * Path 
      ```json
      {
        "id": "7f15dd14-6893-4962-8192-1d6c2fa7e738"
      }
      ```
   * Body: 
      ```json
      {
        "weight": 100,
        "description": "description"
      }  
      ```
   * Response: 
      ```json
      {
        "id": "7f15dd14-6893-4962-8192-1d6c2fa7e738",
        "pick_up": {
          "zip_code": "00601",
          "city": "Adjuntas",
          "state": "Puerto Rico",
          "longitude": -66.75266,
          "latitude": 18.18027,
          "created_date": "2023-05-30T07:08:35.911803"
        },
        "delivery": {
          "zip_code": "00602",
          "city": "Aguada",
          "state": "Puerto Rico",
          "longitude": -67.17541,
          "latitude": 18.36075,
          "created_date": "2023-05-30T07:08:35.911803"
        },
        "weight": 100,
        "description": "description",
        "created_date": "2023-05-30T07:39:23.573880"
      }
      ```
   * Postman 
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][5]][5]
      
     [5]: https://imageup.ru/img232/4357660/welbex_update_cargo.jpg
     </details>
6. Удаление груза
   * Endpoint: **host:port/cargo/{id}**
   * Method: **DELETE**
   * Params:
     * Path 
      ```json
      {
        "id": "7f15dd14-6893-4962-8192-1d6c2fa7e738"
      }
      ```
   * Postman 
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][6]][6]
      
     [6]: https://imageup.ru/img18/4357661/welbex_delete_cargo.jpg
     </details> 

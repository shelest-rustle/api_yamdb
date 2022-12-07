# api_yamdb

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/shelest-rustle/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/Scrpits/activate
```

Обновить pip:

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Сделать и выполнить миграции:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Алгоритм регистрации пользователей и использования токена:
```
Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле
```
```
Отправлять токен нужно при каждом запросе c ключевым словом 'Bearer'
```
____
### Примеры запросов к API:

##### Получение токена
___
```
POST /api/v1/auth/signup/
```

```
Request:
    {
        "email": "user@example.com",
        "username": "string"
    }
Response:
    {
        "username": "string",
        "email": "user@example.com"
    }
```
```
POST /api/v1/auth/token/
```
```
Request:
    {
        "username": "string",
        "confirmation_code": "string"
    }
Response:
    {
        "token": "string"
    }
```
##### Взаимодействие с юзерами
___
```
GET /api/v1/users/
```
```
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {}
        ]
    }
```
```
GET /api/v1/users/{username}/
```
```
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }
```

```
POST /api/v1/users/
```
```
Request:
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }
Response:
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }
```

```
PATCH /api/v1/users/{username}/
```

```
Request:
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }
Respone:
    {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
    }
```

```
DELETE /api/v1/users/{username}/
```
```
```
##### Взаимодействие с произведениями
___
```
GET /api/v1/titles/
```
```
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
            "id": 0,
            "name": "string",
            "year": 0,
            "rating": 0,
            "description": "string",
            "genre": [
                {
                "name": "string",
                "slug": "string"
                }
            ],
            "category": {
                "name": "string",
                "slug": "string"
            }
            }
        ]
    }
```
```
GET /api/v1/titles/{titles_id}/
```
```
    {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
            {
            "name": "string",
            "slug": "string"
            }
        ],
        "category": {
            "name": "string",
            "slug": "string"
        }
    }
```
```
PATCH /api/v1/titles/{titles_id}/
```
```
Request:
    {
        "name": "string",
        "year": 0,
        "description": "string",
        "genre": [
            "string"
        ],
        "category": "string"
    }
Response:
    {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
            {
            "name": "string",
            "slug": "string"
            }
        ],
        "category": {
            "name": "string",
            "slug": "string"
        }
    }
```
```
POST /api/v1/titles/
```
```
Request:
    {
        "name": "string",
        "year": 0,
        "description": "string",
        "genre": [
            "string"
        ],
        "category": "string"
    }
Response:
```
    {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
            {}
        ],
        "category": {
            "name": "string",
            "slug": "string"
        }
    }
```
DELETE /api/v1/titles/{titles_id}/
```
```
```
##### Взаимодействие с категориями
___
```
GET /api/v1/categories/
```
```
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "name": "string",
                "slug": "string"
            }
        ]
    }
```
```
POST /api/v1/categories/
```
```
Request:
    {
        "name": "string",
        "slug": "string"
    }
Response:
    {
        "name": "string",
        "slug": "string"
    }
```
```
DELETE /api/v1/categories/{slug}/
```
```
```
##### Взаимодействие с жанрами
___
```
GET /api/v1/genres/
```
```
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "name": "string",
                "slug": "string"
            }
        ]
    }
```
```
POST /api/v1/genres/
```
```
Request:
    {
        "name": "string",
        "slug": "string"
    }
Response:
    {
        "name": "string",
        "slug": "string"
    }
```
```
DELETE /api/v1/genres/{slug}/
```
```
```
##### Взаимодействие с отзывами
___
```
GET /api/v1/titles/{title_id}/reviews/
```
```
   {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": 0,
          "text": "string",
          "author": "string",
          "score": 1,
          "pub_date": "2019-08-24T14:15:22Z"
        }
      ]
   }
```
```
POST /api/v1/titles/{title_id}/reviews/
```
```
Request:
   {
      "text": "string",
      "score": 1
   }
Response:
   {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
   }
```
```
GET /api/v1/titles/{title_id}/reviews/{review_id}/
```
```
   {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
   }
```
```
PATCH /api/v1/titles/{title_id}/reviews/{review_id}/
```
```
Request:
   {
      "text": "string",
      "score": 1
   }
Response:
   {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
   }
```
```
DELETE /api/v1/titles/{title_id}/reviews/{review_id}/
```
```
```
##### Взаимодействие с комментариями
___
```
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```
   {
      "count": 0,
      "next": "string",
      "previous": "string",
      "results": [
        {
          "id": 0,
          "text": "string",
          "author": "string",
          "pub_date": "2019-08-24T14:15:22Z"
        }
      ]
   }
```
```
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```
Request:
    {
      "text": "string"
    }
Response:
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
```
```
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}
```
```
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
```
```
PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}
```
```
Request:
    {
      "text": "string"
    }
Response:
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
```
```
DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}
```
```
```






## Авторы проекта:
### Шелест Мария
### Лишухай Дмитрий
### Саргис Манукян

# drf_music_api

Api для музыкальной платформы с возможностью загружать треки, создавать альбомы, просматривать контент авторов и подписываться на них

## Установка

Склонируйте репозиторий и перейдите в нужную директорию
```sh
$ git clone https://github.com/v4filippoff/drf_music_api.git
$ cd drf_music_api
```

Запустите докер контейнеры
```sh
$ docker-compose -f docker-compose.yml up -d --build
```

Примените миграции к базе данных и сгенерируйте тестовые данные
```sh
$ docker-compose exec app python manage.py migrate
$ docker-compose exec app python manage.py loaddata test_data.json
```

Ознакомьтесь с документацией к api `http://localhost:8000/swagger/`

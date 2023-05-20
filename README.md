Для запуска:
 - создать в корне проекта папку logs
 - docker-compose build
 - docker-compose up 
 - docker-compose exec app alembic upgrade head

Пример запроса:
 - Метод POST с телом json. Тип application/json
{
  "questions_num": 3 (тип int)
}

Пример ответа:
"Success", status code 201

В этом примере в БД создастся 3 новых записи, если один или несколько вопросов в этом запросе
будут неуникальны, они не будут сохранены в БД, а будут выполняться дополнительные запросы к стороннему АПИ.


Для входа в контейнер с БД:
 - docker-compose exec -it db bash
 - psql -U postgres
 - \connect questions;

Для доступа в SWAGGER:
 - http://0.0.0.0:8010/docs

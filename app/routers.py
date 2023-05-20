import logging
import requests
from fastapi import (
    APIRouter,
    Depends,
)
from app.schemas import (
    QuestionNumber,
    Question,
    Questions,
    QuestionDB
)
from app.models import Table_1
from fastapi.responses import JSONResponse
from app.base import get_session
from sqlalchemy.orm import Session
from sqlalchemy import exc

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/api/v1')


@router.post("/get_number_of_questions", status_code=201)
async def questions_number(
        questions_num: QuestionNumber,
        db_session: Session = Depends(get_session)
) -> JSONResponse:
    if questions_num.questions_num == 0:
        return JSONResponse(content="Empty value for questions_num", status_code=400)

    response = await request_to_api(questions_num.questions_num)

    if response.status_code != 200:
        return JSONResponse(content="Bad request to jservice", status_code=400)

    last_record = db_session.query(Table_1).order_by(Table_1.id.desc()).first()
    if last_record is not None:
        last_question = QuestionDB.from_orm(last_record).q_text
    else:
        last_question = ""

    questions = Questions()
    questions = await create_model_questions(
        questions=questions,
        response_json=response.json()
    )

    i = 0
    while i < len(questions.questions):
        try:
            db_question = Table_1(
                id_from_site=questions.questions[i].id,
                q_text=questions.questions[i].question,
                q_answer=last_question,
                date_created=questions.questions[i].date
            )
            db_session.add(db_question)
            db_session.commit()

            last_question = questions.questions[i].question

        except exc.IntegrityError:
            db_session.rollback()

            response = await request_to_api()

            if response.status_code != 200:
                return JSONResponse(content="Bad request to jservice", status_code=400)

            questions = await create_model_questions(questions, response.json())

        except Exception as e:
            db_session.rollback()
            return JSONResponse(content=f"Error with DB, cause {str(e)}", status_code=400)

        finally:
            i += 1

    return JSONResponse(content='Success', status_code=201)


async def request_to_api(
        questions_num: int = 1
) -> requests.models.Response:
    response = requests.get(f'https://jservice.io/api/random?count={questions_num}')

    return response


async def create_model_questions(
        questions: Questions,
        response_json: dict
) -> Questions:
    for i in response_json:
        question_for_db = Question(id=i['id'], question=i['question'], date=i['created_at'])
        questions.questions.append(question_for_db)

    return questions

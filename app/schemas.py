import datetime
from typing import List
from pydantic import BaseModel


class QuestionNumber(BaseModel):
    questions_num: int


class Question(BaseModel):
    id: int
    question: str
    date: datetime.datetime


class Questions(BaseModel):
    questions: List[Question] = []


class QuestionDB(BaseModel):
    id: int
    id_from_site: int
    q_text: str
    q_answer: str
    date_created: datetime.datetime

    class Config:
        orm_mode = True


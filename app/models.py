from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Table_1(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    id_from_site = Column(Integer, unique=True)
    q_text = Column(Text)
    q_answer = Column(Text)
    date_created = Column(DateTime(timezone=True))

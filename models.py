from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, index=True)
    fname=Column(String)
    lname=Column(String)
    email=Column(String)
    password=Column(String)
    age=Column(Integer)
    number=Column(Integer)
    Questions_asked = relationship("Questions", back_populates="question_owner")
    Answers_posted = relationship("Answers", back_populates="answer_owner")

class Questions(Base):
    __tablename__='Questions'
    id = Column(Integer, primary_key=True, index=True)
    title=Column(String)
    body=Column(String)
    user_id=Column(Integer, ForeignKey('Users.id'))
    question_owner = relationship("User", back_populates="Questions_asked")


class Answers(Base):
    __tablename__='Answers'
    id = Column(Integer, primary_key=True, index=True)
    title=Column(String)
    body=Column(String)
    user_id=Column(Integer, ForeignKey('Users.id'))
    answer_owner = relationship("User", back_populates="Answers_posted")





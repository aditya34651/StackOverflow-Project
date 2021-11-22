from sqlalchemy import Column, Integer, String, ForeignKey, Table
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
    user_tags = relationship("Tags", back_populates="tag_owner")
    owner_comments = relationship("Comments", back_populates="comment_author")


question_tags = Table("question_tags", Base.metadata,
                   Column("question_id", ForeignKey("Questions.id"), primary_key=True),
                   Column("tag_id", ForeignKey("Tags.id"), primary_key=True))


class Questions(Base):
    __tablename__='Questions'
    id = Column(Integer, primary_key=True, index=True)
    title=Column(String)
    body=Column(String)
    user_id=Column(Integer, ForeignKey('Users.id'))
    question_owner = relationship("User", back_populates="Questions_asked")
    question_comments = relationship("Comments", back_populates="comments_to_question")
    tags_q = relationship("Tags", secondary=question_tags, back_populates="questions_s")
    answers_to_the_ques = relationship("Answers", back_populates="question_of_ans")



class Answers(Base):
    __tablename__='Answers'
    id = Column(Integer, primary_key=True, index=True)
    title=Column(String)
    body=Column(String)
    user_id=Column(Integer, ForeignKey('Users.id'))
    ques_id = Column(Integer, ForeignKey('Questions.id'))
    answer_owner = relationship("User", back_populates="Answers_posted")
    answer_comments = relationship("Comments", back_populates="comments_to_answer")
    question_of_ans = relationship("Questions", back_populates="answers_to_the_ques")

class Tags(Base):
    __tablename__='Tags'
    id = Column(Integer, primary_key=True, index=True)
    tagname=Column(String)
    tag_owner_id = Column(Integer, ForeignKey('Users.id')) 
    questions_s = relationship("Questions", secondary=question_tags, back_populates="tags_q")
    tag_owner = relationship("User", back_populates="user_tags")


class Comments(Base):
    __tablename__='Comments'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String) 
    answer_id = Column(Integer, ForeignKey('Answers.id'))
    question_id = Column(Integer, ForeignKey('Questions.id'))
    user_id = Column(Integer, ForeignKey('Users.id'))
    comments_to_answer = relationship("Answers", back_populates="answer_comments")
    comments_to_question = relationship("Questions", back_populates="question_comments")
    comment_author = relationship("User", back_populates="owner_comments")






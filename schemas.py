from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import FastAPI, Query


class Questions(BaseModel):
    title:str
    body:str
    user_id:int
    class Config():
        orm_mode = True


class Answers(BaseModel):
    title:str
    body:str
    user_id:int   
    class Config():
        orm_mode = True
 

class User(BaseModel):
    fname:str = Query(..., max_length=50)  
    lname:str  = Query(..., max_length=50) 
    email:str 
    password:str=Query(..., max_length=12) 
    age:Optional[int] = Field(None)
    number:int = Field(..., lt=11)

class User2(BaseModel):
     fname:str
     lname:str
     class Config():
        orm_mode = True

class ShowUsers(BaseModel):
    fname:str
    lname:str  
    Questions_asked:List[Questions]
    Answers_posted:List[Answers]
    class Config():
        orm_mode = True

class ShowQues(BaseModel):
    title:str
    body:str
    question_owner: User2 
    class Config():
        orm_mode=True

class ShowAns(BaseModel):
     title:str
     body:str
     answer_owner: ShowUsers
     class Config():
        orm_mode=True

class Login(BaseModel):
     username:str
     password:str       

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

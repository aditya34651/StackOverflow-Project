from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import FastAPI, Query


class Questions(BaseModel):
    title:str
    body:str
    user_id:int
    class Config():
        orm_mode = True

class UpdateQues(BaseModel):
    title:str
    body:str



class Answers(BaseModel):
    title:str
    body:str
    user_id:int
    ques_id:int   
    class Config():
        orm_mode = True

class UpdateAns(BaseModel):
    title:str
    body:str
 

class User(BaseModel):
    fname:str = Query(..., max_length=50)  
    lname:str  = Query(..., max_length=50) 
    email:str = Query(..., regex="^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", description="Invalid format of the email!")
    password:str=Query(..., max_length=12) 
    age:Optional[int] = None
    number:int = Field(..., lt=99999999999)

class User2(BaseModel):
     fname:str
     lname:str
     class Config():
        orm_mode = True

class ShowUsers(BaseModel):
    id: str
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
     answer_owner: User2
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

class Tags(BaseModel):
    tagname:str
    tag_owner_id:int    
    class Config():
        orm_mode=True


class Comments(BaseModel):
    description:str
    user_id:int
    ques_id:int 
    class Config():
        orm_mode = True  
     

class Comments2(BaseModel):
    description:str
    class Config():
        orm_mode=True

class Comments3(BaseModel):
    description:str
    ques_id:int
    class Config():
        orm_mode=True
        

class Showcomm(BaseModel):
    description:str
    id:str

    class Config():
        orm_mode=True

class ShowTags(BaseModel):
    tagname:str
    id:str

    class Config():
        orm_mode=True

class TagsQues(Tags):
    questions_s: List[Questions]

class QuesTags(Questions):
    tags_q: List[Tags]
    
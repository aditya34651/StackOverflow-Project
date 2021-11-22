from fastapi import APIRouter, Depends,status,HTTPException,Response
import schemas, database, models, oauth2, JWTtoken
from typing import List
from sqlalchemy.orm import Session
from hashing import Hash
from jose import jwt

router = APIRouter()
get_db = database.get_db



@router.get('/comments', response_model=List[schemas.Showcomm],tags=['Comments'])
def GetAllComments(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Comments).all()
    return ques  

@router.post('/question/{id}/comments', status_code=status.HTTP_201_CREATED, tags=['Comments'])
def PostQuestionComment(id, request:schemas.Comments2, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user),token:str=Depends(oauth2.oauth2_scheme)):
    try:
        payload=jwt.decode(token, JWTtoken.SECRET_KEY, algorithms=JWTtoken.ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
        user = db.query(models.User).filter(models.User.email==username).first()    
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

    ques = db.query(models.Questions).filter(models.Questions.id == id)
    if not ques.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ques does not exist")
    else:
        user_id = user.id
        new_comm = models.Comments(description=request.description, user_id=user_id,question_id=id)
        db.add(new_comm)
        db.commit()
        db.refresh(new_comm)
        return new_comm
 
 
@router.post('/answers/{id}/comments', status_code=status.HTTP_201_CREATED, tags=['Comments'])
def PostAnswerComment(id, request:schemas.Comments2, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user),token:str=Depends(oauth2.oauth2_scheme)):
    try:
        payload=jwt.decode(token, JWTtoken.SECRET_KEY, algorithms=JWTtoken.ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
        user = db.query(models.User).filter(models.User.email==username).first()    
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

    ans = db.query(models.Answers).filter(models.Answers.id == id)
    if not ans.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ans does not exist")
    else:
        user_id = user.id
        new_comm = models.Comments(description=request.description, user_id=user_id,answer_id=id)
        db.add(new_comm)
        db.commit()
        db.refresh(new_comm)
        return new_comm

@router.delete('/comments/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Comments'])
def DeleteComments(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user),token:str=Depends(oauth2.oauth2_scheme)): 
    try:
        payload=jwt.decode(token, JWTtoken.SECRET_KEY, algorithms=JWTtoken.ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
        user = db.query(models.User).filter(models.User.email==username).first()    
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

    ques = db.query(models.Comments).filter(models.Comments.id == id)
    if not ques.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"comment does not exist")
    if ques.first().user_id == user.id:    
        ques.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
 

@router.put('/comments/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['Comments'])
def UpdateComments(id, request:schemas.Comments2, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user),token:str=Depends(oauth2.oauth2_scheme)):
    try:
        payload=jwt.decode(token, JWTtoken.SECRET_KEY, algorithms=JWTtoken.ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
        user = db.query(models.User).filter(models.User.email==username).first()    
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
   
    ques = db.query(models.Comments).filter(models.Comments.id == id)
    if not ques.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"comment does not exist")
    if ques.first().user_id == user.id:    
        ques.update(request.dict())
        db.commit()
        return Response(status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
      

      
@router.get('/comments/{id}', status_code=200, response_model=schemas.Comments3,tags=['Comments'])
def GetCommentsByID(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Comments).filter(models.Comments.id == id).first()  
    if not ques:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"comment with the id {id} does not exist")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'details': f"ques with the id {id} does not exist"}
    return ques   
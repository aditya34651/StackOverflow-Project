from fastapi import APIRouter, Depends,status,HTTPException, Response
import schemas, database, models, oauth2, JWTtoken
from typing import List
from sqlalchemy.orm import Session
from hashing import Hash
from jose import jwt

router = APIRouter()
get_db = database.get_db



@router.post('/questions/{id}/answers', status_code=status.HTTP_201_CREATED,tags=['Answers'])
def CreateAnswer(id, request: schemas.UpdateAns, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user),token:str=Depends(oauth2.oauth2_scheme)):
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

    ques = db.query(models.Questions).filter(models.Questions.id ==id)
    if not ques.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ques does not exist")
    else:
        user_id = user.id
        new_ans = models.Answers(title=request.title, body=request.body, user_id=user_id , ques_id = id)
        db.add(new_ans)
        db.commit()
        db.refresh(new_ans)
        return new_ans

@router.delete('answers/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=['Answers'])
def DeleteAns(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user), token:str=Depends(oauth2.oauth2_scheme)):
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
    if ans.first().user_id == user.id:    
        ans.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)



@router.put('/answers/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Answers'])
def update(id, request: schemas.UpdateAns, db: Session= Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    
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
   
    ans=db.query(models.Answers).filter(models.Answers.id == id)
    if not ans.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ans does not exist")
    if ans.first().user_id == user.id:    
        ans.update(request.dict())
        db.commit()
        return Response(status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
      

@router.get('/answers', response_model=List[schemas.ShowAns], tags=['Answers'])
def all(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ans = db.query(models.Answers).all()
    return ans


@router.get('/answers/{id}', status_code=200, response_model=schemas.ShowAns, tags=['Answers'])
def show(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ans = db.query(models.Answers).filter(models.Answers.id == id).first()  
    if not ans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"ans with the id {id} does not exist")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'details': f"ans with the id {id} does not exist"}
    return ans  
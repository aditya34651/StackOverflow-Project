from fastapi import APIRouter, Depends,status,HTTPException, Response
import schemas, database, models, oauth2, JWTtoken
from typing import  List
from sqlalchemy.orm import Session
from jose import jwt
get_db = database.get_db

router = APIRouter()


@router.get('/questions', response_model=List[schemas.ShowQues],tags=['Questions'])
def all(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Questions).all()
    return ques  

@router.post('/questions', status_code=status.HTTP_201_CREATED, tags=['Questions'])
def question(request:schemas.UpdateQues, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user), token:str=Depends(oauth2.oauth2_scheme)):
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

    user_id = user.id
    new_ques = models.Questions(title=request.title, body=request.body, user_id=user_id)
    db.add(new_ques)
    db.commit()
    db.refresh(new_ques)
    return new_ques


@router.delete('/questions/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Questions'])
def destroy(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user), token:str = Depends(oauth2.oauth2_scheme)):
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
    if ques.first().user_id == user.id:    
        ques.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)



@router.put('/questions/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['Questions'])
def update(id, request:schemas.UpdateQues, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user),token:str = Depends(oauth2.oauth2_scheme)):
    
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
    if ques.first().user_id == user.id:    
        ques.update(request.dict())
        db.commit()
        return Response(status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    

@router.get('/questions/{id}', status_code=200, response_model=schemas.ShowQues,tags=['Questions'])
def show(id, db:Session = Depends(get_db)):
    ques = db.query(models.Questions).filter(models.Questions.id == id).first()  
    if not ques:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"ques with the id {id} does not exist")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'details': f"ques with the id {id} does not exist"}
    return ques   
from fastapi import APIRouter, Depends,status,HTTPException, Response
import schemas, database, models, oauth2, JWTtoken
from typing import  List
from sqlalchemy.orm import Session
from hashing import Hash
from jose import jwt

router = APIRouter()
get_db = database.get_db




@router.get('/tags', response_model=List[schemas.ShowTags],tags=['Tags'])
def all(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user), token:str=Depends(oauth2.oauth2_scheme)):
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
    ques = db.query(models.Tags).filter(models.Tags.tag_owner_id==user_id).all()
    return ques  
    

@router.post('/tags', status_code=status.HTTP_201_CREATED, tags=['Tags'])
def Newtag(id, request:schemas.Tags, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user),token:str=Depends(oauth2.oauth2_scheme)):
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


    tag_owner_id = user.id
    new_comm = models.Tags(tagname=request.tagname, tag_owner_id=tag_owner_id)
    db.add(new_comm)
    db.commit()
    db.refresh(new_comm)

@router.delete('/tags/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Tags'])
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

   
    ques = db.query(models.Tags).filter(models.Tags.id == id)
    if not ques.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag does not exist")
    if ques.first().tag_owner_id == user.id:    
        ques.delete()
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
  

@router.put('/tags/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['Tags'])
def update(id, request:schemas.Tags, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user), token:str = Depends(oauth2.oauth2_scheme)):
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
   
    ques = db.query(models.Tags).filter(models.Tags.id == id)
    if not ques.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag does not exist")
    if ques.first().tag_owner_id == user.id:    
        ques.update(request.dict())
        db.commit()
        return Response(status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
  

@router.get('/tags/{id}', status_code=200, response_model=schemas.ShowQues,tags=['Tags'])
def show(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Tags).filter(models.Tags.id == id).first()  
    if not ques:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"ques with the id {id} does not exist")
    return ques   
from fastapi import APIRouter, Depends,status,HTTPException
import schemas, database, models, oauth2
from typing import  List
from sqlalchemy.orm import Session
from hashing import Hash

router = APIRouter()
get_db = database.get_db



@router.post('/user',status_code=status.HTTP_201_CREATED, tags=['Users'])
def CreateU(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(fname=request.fname, lname=request.lname, email=request.email, password=Hash.bcrypt(request.password), age=request.age, number=request.number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/userList', response_model=List[schemas.ShowUsers], tags=['Users'])
def showusers(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    Users = db.query(models.User).all()
    return Users   

@router.get('/userList/{id}',  status_code=200, response_model=schemas.ShowUsers, tags=['Users'])   
def show(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"User with the id {id} does not exist" )
    return user

    
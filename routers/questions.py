from fastapi import APIRouter, Depends,status,HTTPException
import schemas, database, models, oauth2
from typing import  List
from sqlalchemy.orm import Session
get_db = database.get_db

router = APIRouter()


@router.get('/questions', response_model=List[schemas.ShowQues],tags=['Questions'])
def all(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Questions).all()
    return ques  

@router.post('/questions', status_code=status.HTTP_201_CREATED, tags=['Questions'])
def question(request:schemas.Questions, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_ques = models.Questions(title=request.title, body=request.body, user_id=request.user_id)
    db.add(new_ques)
    db.commit()
    db.refresh(new_ques)
    return new_ques


@router.delete('/questions/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Questions'])
def destroy(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Questions).filter(models.Questions.id == id)
    if not ques.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ques does not exist")
    ques.delete()
    db.commit()
    return 'Deleted'      

@router.put('/questions/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['Questions'])
def update(id, request:schemas.Questions, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Questions).filter(models.Questions.id == id)
    if not ques.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ques does not exist")
    ques.update(request.dict())
    db.commit()
    return 'updated successfully'

@router.get('/questions/{id}', status_code=200, response_model=schemas.ShowQues,tags=['Questions'])
def show(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Questions).filter(models.Questions.id == id).first()  
    if not ques:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"ques with the id {id} does not exist")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'details': f"ques with the id {id} does not exist"}
    return ques   
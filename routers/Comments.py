from fastapi import APIRouter, Depends,status,HTTPException
import schemas, database, models, oauth2
from typing import  List
from sqlalchemy.orm import Session
get_db = database.get_db

router = APIRouter()


@router.get('/comments', response_model=List[schemas.Showcomm],tags=['Comments'])
def all(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Comments).all()
    return ques  

@router.post('/comments', status_code=status.HTTP_201_CREATED, tags=['Comments'])
def comment(request:schemas.Comments, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_comm = models.Comments(description=request.description)
    db.add(new_comm)
    db.commit()
    db.refresh(new_comm)
    return new_comm


@router.delete('/comments/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Comments'])
def destroy(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Comments).filter(models.Comments.id == id)
    if not ques.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ques does not exist")
    ques.delete()
    db.commit()
    return 'Deleted'      

@router.put('/comments/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['Comments'])
def update(id, request:schemas.Comments, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Comments).filter(models.Comments.id == id)
    if not ques.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ques does not exist")
    ques.update(request.dict())
    db.commit()
    return 'updated successfully'

@router.get('/comments/{id}', status_code=200, response_model=schemas.ShowQues,tags=['Comments'])
def show(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Comments).filter(models.Comments.id == id).first()  
    if not ques:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"ques with the id {id} does not exist")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'details': f"ques with the id {id} does not exist"}
    return ques   
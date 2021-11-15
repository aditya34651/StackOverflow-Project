from fastapi import APIRouter, Depends,status,HTTPException
import schemas, database, models, oauth2
from typing import  List
from sqlalchemy.orm import Session
get_db = database.get_db

router = APIRouter()



@router.get('/tags', response_model=List[schemas.ShowTags],tags=['Tags'])
def all(db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Tags).all()
    return ques  

@router.post('/tags', status_code=status.HTTP_201_CREATED, tags=['Tags'])
def comment(request:schemas.Tags, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_comm = models.Tags(description=request.description)
    db.add(new_comm)
    db.commit()
    db.refresh(new_comm)
    return new_comm


@router.delete('/tags/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Tags'])
def destroy(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Tags).filter(models.Tags.id == id)
    if not ques.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ques does not exist")
    ques.delete()
    db.commit()
    return 'Deleted'      

@router.put('/tags/{id}', status_code=status.HTTP_202_ACCEPTED,tags=['Tags'])
def update(id, request:schemas.Tags, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Tags).filter(models.Tags.id == id)
    if not ques.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ques does not exist")
    ques.update(request.dict())
    db.commit()
    return 'updated successfully'

@router.get('/tags/{id}', status_code=200, response_model=schemas.ShowQues,tags=['Tags'])
def show(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ques = db.query(models.Tags).filter(models.Tags.id == id).first()  
    if not ques:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"ques with the id {id} does not exist")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'details': f"ques with the id {id} does not exist"}
    return ques   
from fastapi import APIRouter, Depends,status,HTTPException
import schemas, database, models, oauth2
from typing import  List
from sqlalchemy.orm import Session
from hashing import Hash

router = APIRouter()
get_db = database.get_db



@router.post('/answers', status_code=status.HTTP_201_CREATED,tags=['Answers'])
def CreateAnswer(request: schemas.Answers, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_ans = models.Answers(title=request.title, body=request.body, user_id=request.user_id )
    db.add(new_ans)
    db.commit()
    db.refresh(new_ans)
    return new_ans

@router.delete('answers/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=['Answers'])
def DeleteAns(id, db:Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ans = db.query(models.Answers).filter(models.Answers.id == id)
    if  not ans.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Answers does not exist")
    ans.delete()
    db.commit()
    return 'Deleted Successfully'

@router.put('/answers/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Answers'])
def update(id, request: schemas.Answers, db: Session= Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    ans=db.query(models.Answers).filter(models.Answers.id == id)
    if not ans.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Answers Does not exist{id}")
    ans.update(request.dict())
    db.commit()
    return 'updated successfully'        

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
from fastapi import FastAPI
import schemas,models
from database import engine
from routers import questions, user,answer, authentication


#Changes


app = FastAPI()

models.Base.metadata.create_all(engine)
app.include_router(questions.router)
app.include_router(user.router)
app.include_router(answer.router)
app.include_router(authentication.router)
 


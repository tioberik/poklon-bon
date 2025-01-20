from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
from ..hashing import Hash
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    tags=["Auth"]
)

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):

    user =  db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Korisnik ne postoji")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Korisnik ne postoji")
    
    #access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}
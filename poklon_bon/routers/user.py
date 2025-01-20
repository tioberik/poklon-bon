from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..hashing import Hash
from ..oauth2 import get_current_user

router =  APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("")
def create_user(request: schemas.User, db : Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    new_user = models.User(
        username=request.username,
        password=Hash.bcrypt(request.password)
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is already taken")

    return new_user
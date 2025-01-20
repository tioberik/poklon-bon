from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database
from sqlalchemy.orm import Session
from typing import List
from ..repository import bon
from ..oauth2 import get_current_user

router =  APIRouter(
    prefix="/bonovi",
    tags=["Poklon bon"]
)


@router.get("", response_model=List[schemas.ShowBon],)
def all(db : Session = Depends(database.get_db)):
    return bon.get_all(db)


@router.get("/{id}", status_code=200, response_model=schemas.ShowBon,)
def show(id, db : Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return bon.show_bon(id, db)


@router.post("", status_code=status.HTTP_201_CREATED)
def create(request: schemas.PoklonBon, db : Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return bon.create_bon(request, db, current_user)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.UpdateBon ,db : Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return bon.update_bon(id, request, db)
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db : Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    return bon.delete_bon(id, db)
from fastapi import HTTPException, status
from .. import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def get_all(db: Session):
    bonovi = db.query(models.PoklonBon).all()
    return bonovi

def create_bon(request: schemas.PoklonBon, db: Session, current_user: schemas.User):
    try:
        new_bon = models.PoklonBon(
            barcode=request.barcode,
            value=request.value,
            user_id=1,
            customer_name=request.customer_name
        )
        db.add(new_bon)
        db.commit()
        db.refresh(new_bon)
        return new_bon
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Barcode already exists")
    
def show_bon(id: int, db: Session): 
    bon = db.query(models.PoklonBon).filter(models.PoklonBon.id == id).first()
    if not bon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bon sa id brojem {id} ne postoji")
    return bon

def update_bon(id: int, request: schemas.PoklonBon, db: Session):
    bon = db.query(models.PoklonBon).filter(models.PoklonBon.id == id)
    if not bon.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bon sa id brojem {id} ne postoji")
    bon_data = request.model_dump(exclude_unset=True)
    bon.update(bon_data)
    db.commit()
    return {"status" : "Updated!"}

def delete_bon(id: int, db: Session):
    bon = db.query(models.PoklonBon).filter(models.PoklonBon.id == id)
    if not bon.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bon sa id brojem {id} ne postoji")
    bon.delete(synchronize_session=False)
    db.commit()
    return {"status" : "Deleted!"}
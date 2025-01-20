from fastapi import HTTPException, status
from .. import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..redis_cache import redis_client
import json

def get_all(db: Session):
    cached_bonovi = redis_client.get("all_bonovi")
    if cached_bonovi:
        return json.loads(cached_bonovi)

    bonovi = db.query(models.PoklonBon).all()

    # Pretvaranje SQLAlchemy objekata u listu slovara (dict) pomoću Pydantic sheme
    bonovi_data = [schemas.ShowBon.model_validate(bon).model_dump() for bon in bonovi]

    # Konverzija datuma u JSON serializable format
    for bon in bonovi_data:
        bon["expires_at"] = bon["expires_at"].isoformat() if bon["expires_at"] else None

    # Keširanje podataka u Redis na 5 minuta (300 sekundi)
    redis_client.setex("all_bonovi", 300, json.dumps(bonovi_data))

    return bonovi_data


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

        # Brisanje keša kako bi sledeći poziv dobio nove podatke
        redis_client.delete("all_bonovi")

        return new_bon
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Barcode already exists")

    
def show_bon(id: int, db: Session):
    cached_bon = redis_client.get(f"bon_{id}")
    if cached_bon:
        return json.loads(cached_bon)

    bon = db.query(models.PoklonBon).filter(models.PoklonBon.id == id).first()
    if not bon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bon sa id brojem {id} ne postoji")

    # Konvertujemo SQLAlchemy objekat u Pydantic model i serijalizujemo u dict
    bon_instance = schemas.ShowBon.model_validate(bon)
    bon_data = bon_instance.model_dump()

    # Konverzija datetime objekata u string prije serijalizacije
    bon_data["expires_at"] = bon_data["expires_at"].isoformat()

    redis_client.setex(f"bon_{id}", 600, json.dumps(bon_data))  # Keširanje na 10 minuta
    
    return bon_instance

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
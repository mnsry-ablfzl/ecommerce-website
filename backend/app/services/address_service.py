from sqlalchemy.orm import Session
from app.db.models.address import Address
from app.schemas.address import AddressCreate

def create_address(user_id: int, payload: AddressCreate, db: Session):
    if payload.is_default:
        db.query(Address).filter(
            Address.user_id == user_id,
            Address.address_type == payload.address_type
        ).update({"is_default": False})

    address = Address(user_id=user_id, **payload.dict())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def list_addresses(user_id: int, db: Session):
    return db.query(Address).filter(Address.user_id == user_id).all()


def delete_address(user_id: int, address_id: int, db: Session):
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()

    if not address:
        return False

    db.delete(address)
    db.commit()
    return True

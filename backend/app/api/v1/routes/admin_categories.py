from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_admin_user
from app.db.session import get_db
from app.db.models.category import Categroy

router = APIRouter()


@router.post("/")
def create_category(name: str, db: Session = Depends(get_db), admin = Depends(get_admin_user)):
    category = Categroy(name=name)
    db.add(category)
    db.commit()
    return {"id": category.id, "name": category.name}


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), admin = Depends(get_admin_user)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}

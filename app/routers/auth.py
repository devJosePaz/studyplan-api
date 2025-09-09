from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db, Base, engine
from app.models import User
from app.schemas import RegisterIn, TokenOut
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenOut)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == data.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user = User(email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    token = create_access_token(sub=user.email)
    return TokenOut(access_token=token)

@router.post("/login", response_model=TokenOut)
def login(data: RegisterIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = create_access_token(sub=user.email)
    return TokenOut(access_token=token)

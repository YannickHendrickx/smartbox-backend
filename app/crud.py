# Imports
from sqlalchemy.orm import Session
import auth, models, schemas

# Get user
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Get user by name
def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

# Get all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# get user by provided id
def get_user(db: Session, user_id: int):
    user_by_id = db.query(models.User).filter(models.User.id == user_id).first()
    return user_by_id

# Add new user
def create_user(db: Session, user: schemas.userAdd):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete specific user
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

# Update specific user
def update_user(db: Session, user_id: int, user: schemas.userAdd):
    hashed_password = auth.get_password_hash(user.password)
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.name = user.name
    db_user.password = hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user
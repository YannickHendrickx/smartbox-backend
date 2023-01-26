#!/usr/bin/python3

# Imports
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import crud, models, schemas, auth
import RPi.GPIO as GPIO
import time
import os

# make database dir if it doesn't exist
if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

# create tables in database 'sqlitedata.db' (check datapase.py database-URL)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# make database session/connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# allowed origins for CORS
origins = ["*"]

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

# Add authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #Try to authenticate the user
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT case sub with the subject(user)
    access_token = auth.create_access_token(
        data={"sub": user.name}
    )
    #Return the JWT as a bearer token to be placed in the headers
    return {"access_token": access_token, "token_type": "bearer"}

# Get information about current logged in user
@app.get("/users/me", response_model=schemas.user)
async def read_users_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = auth.get_current_active_user(db, token)
    return current_user

# Add new user
@app.post("/users/", response_model=schemas.user)
async def create_user(user: schemas.userAdd, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

# Get all users
@app.get("/users/", response_model=list[schemas.user])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Get specific user
@app.get("/users/{user_id}", response_model=schemas.user)
async def read_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return db_user

# Delete specific user
@app.delete("/users/{user_id}", response_model=schemas.user)
async def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return db_user

# Update specific user
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: schemas.userAdd, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_user = crud.update_user(db, user_id=user_id, user=user)
    return db_user

# Get specific user
@app.get("/users/code/{user_access_code}", response_model=schemas.user)
async def read_user(user_access_code: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_access_code=user_access_code)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return db_user

@app.get("/lock/")
async def control_lock():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    deur_1 = 17

    GPIO.setup(deur_1, GPIO.OUT)
    GPIO.output(deur_1, 1)

    def deur_1_openen():
        print("deur open")
        GPIO.output(deur_1, 0)
        time.sleep(0.1)
        GPIO.output(deur_1, 1)

    while true:
        deur_1_openen()
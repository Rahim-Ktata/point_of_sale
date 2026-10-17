
from fastapi import FastAPI, Depends, status, HTTPException
from app import models, schemas

from sqlalchemy.orm import Session

from app.dependencies import DbDep


def add_error(db: DbDep, text):
    try:
        error = models.Error(text=text)
        db.add(error)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="something went wrong!")

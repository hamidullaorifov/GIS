from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.orm import Session
from pydantic import HttpUrl

from app.schemas import maps as map_schemas, users as user_schemas
from app.db.setup import get_db
from app.services import mapservices
from app.services.auth import get_current_user




router = APIRouter(tags=['Maps'])




@router.post("/maps/", response_model=map_schemas.Map, status_code=201)
def create_map(map: map_schemas.MapCreate, db: Session = Depends(get_db), current_user: user_schemas.User = Depends(get_current_user)):
    
    created_map = mapservices.create_map(db=db, map=map, user_id=current_user.id)
    
    return created_map.to_schema()

@router.get("/maps/", response_model=List[map_schemas.Map])
def read_maps(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    
    maps = mapservices.get_maps(db, skip=skip, limit=limit)
    response_data = [map.to_schema() for map in maps]
    
    return response_data

@router.get("/maps/{map_id}", response_model=map_schemas.Map)
def read_map(map_id: int, db: Session = Depends(get_db)):
    db_map = mapservices.get_map(db, map_id=map_id)
    if db_map is None:
        raise HTTPException(status_code=404, detail="Map not found")
    return db_map.to_schema()

@router.put("/maps/{map_id}", response_model=map_schemas.Map)
def update_map(map_id: int, map: map_schemas.MapCreate, db: Session = Depends(get_db), current_user: user_schemas.User = Depends(get_current_user)):
    updated_map = mapservices.update_map(db=db, map=map, map_id=map_id, user_id=current_user.id)
    
    return updated_map.to_schema()

@router.delete("/maps/{map_id}", status_code=204)
def delete_map(map_id: int, db: Session = Depends(get_db), current_user: user_schemas.User = Depends(get_current_user)):
    
    mapservices.delete_map(db=db, map_id=map_id, user_id=current_user.id)

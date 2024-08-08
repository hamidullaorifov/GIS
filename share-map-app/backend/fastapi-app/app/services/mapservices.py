from sqlalchemy.orm import Session
from app.db import models
from app.schemas import maps

def create_map(db: Session, map: maps.MapCreate, user_id: int):
    
    db_map = map.to_model(user_id)
    db.add(db_map)
    db.commit()
    db.refresh(db_map)
    return db_map

def get_maps(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Map).offset(skip).limit(limit).all()

def get_map(db: Session, map_id: int):
    return db.query(models.Map).filter(models.Map.id == map_id).first()

def update_map(db: Session, map: maps.MapCreate, map_id: int, user_id: int):

    db_map = get_map(db, map_id)

    if db_map is None or db_map.creator_id != user_id:
        return None
    for key, value in map.model_dump(exclude_unset=True, exclude=('action_button',)).items():
        setattr(db_map, key, value)
    setattr(db_map,'action_button_url',str(map.action_button.url))
    setattr(db_map,'action_button_text',map.action_button.button_text)
    setattr(db_map,'action_button_open_link_in',map.action_button.open_link_in)
    db.commit()
    db.refresh(db_map)
    return db_map

def delete_map(db: Session, map_id: int, user_id: int):
    db_map = get_map(db, map_id)
    if db_map is None or db_map.creator_id != user_id:
        return None
    db.delete(db_map)
    db.commit()
    return db_map
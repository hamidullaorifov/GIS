from pydantic import BaseModel, HttpUrl
from enum import Enum

from app.db import models

class MapView(str, Enum):
    autofit = "autofit"
    center = "center"
    area = "area"

class ContentPanelView(str, Enum):
    desktop = "desktop"
    mobile = "mobile"

class OpenLinkIn(str, Enum):
    new_tab = "new_tab"
    same_tab = "same_tab"
    modal = "modal"

class ActionButton(BaseModel):
    url: HttpUrl
    button_text: str
    open_link_in: OpenLinkIn


class MapBase(BaseModel):
    title: str
    description: str
    action_button: ActionButton
    default_map_view: MapView
    default_content_panel_view: ContentPanelView
    display_category_legend: bool

class MapCreate(MapBase):

    def to_model(self,user_id):
        action_button = self.action_button
        
        return models.Map(
            **self.model_dump(exclude=('action_button',)), 
            creator_id = user_id,
            action_button_url = str(action_button.url),
            action_button_text = action_button.button_text,
            action_button_open_link_in = action_button.open_link_in
            )

class Map(MapBase):
    id: int
    creator_id: int

    class Config:
        orm_mode = True

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    user_id: Optional[str]
    password: str


class User(UserBase, table=True):
    user_id: Optional[str] = Field(default=None, primary_key=True)
    password: str
    nickname: str
    created_at: datetime = Field(default_factory=datetime.today)

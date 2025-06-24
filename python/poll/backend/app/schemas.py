from pydantic import BaseModel

class OptionBase(BaseModel):
    id: int
    text: str
    votes: int

    class Config:
        orm_mode = True

class PollBase(BaseModel):
    id: int
    title: str
    options: list[OptionBase]
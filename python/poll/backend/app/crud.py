from sqlalchemy.orm import Session
from . import models

def get_poll(db: Session, poll_id: int):
    poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    if poll:
        options = db.query(models.Option).filter(models.Option.poll_id == poll_id).all()
        poll.options = options
    return poll

def increment_vote(db: Session, option_id: int):
    option = db.query(models.Option).filter(models.Option.id == option_id).first()
    if option:
        option.votes += 1
        db.commit()
        db.refresh(option)
        return option
    return None
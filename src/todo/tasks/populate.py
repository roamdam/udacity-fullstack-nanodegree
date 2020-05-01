from models import Item
from todo import db
from sqlalchemy.exc import IntegrityError


def populate_items():
    """Reset Items table and populate it (not used)."""
    Item.__table__.drop(db.engine, checkfirst=True)
    Item.__table__.create(db.engine, checkfirst=True)

    new_items = [
        Item(text='Task 1'),
        Item(text='Task 2', due_date='2020-05-01')
    ]

    db.session.add_all(new_items)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

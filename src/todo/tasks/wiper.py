
from todo import db
from models import Item


class Wiper:
    """Controller to delete all to do items at once."""

    @staticmethod
    def clear():
        Item.query.delete()
        db.session.commit()

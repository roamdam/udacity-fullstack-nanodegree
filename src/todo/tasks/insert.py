
from todo import db
from flask import abort
from logging import getLogger
from psycopg2 import Error
from models import Item


class ItemWriter:
    """Controller for writing new to-do items into database."""

    @staticmethod
    def __nonify_date__(data: dict) -> None:
        """Set missing due date to None."""
        if len(data['due-date']) == 0:
            data['due-date'] = None

    @staticmethod
    def insert(data: dict) -> None:
        """Handle POST request data to create a new row into items table."""
        ItemWriter.__nonify_date__(data=data)
        new_item = Item(
            text=data['text'],
            due_date=data['due-date']
        )
        try:
            db.session.add(new_item)
        except Error as e:
            db.session.rollback()
            getLogger(__name__).error(e)
            abort(500)
        else:
            db.session.commit()
        finally:
            db.session.close()

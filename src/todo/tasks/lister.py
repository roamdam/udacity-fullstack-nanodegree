from models import Item


class ItemLister:
    """Controller to get all to do items from database."""

    @staticmethod
    def get_all() -> list:
        return Item.query.all()

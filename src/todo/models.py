from todo import db


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"Item(text={self.text}, due_date={self.due_date})"

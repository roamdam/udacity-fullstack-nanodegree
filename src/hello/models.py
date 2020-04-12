from hello import db
from re import sub


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String(4), nullable=False, default='OOOO')

    def __repr__(self):
        """Build a repr of the form User(key1 : value1, key2: value2, ...)."""
        this_repr = "User("
        for key, value in self.__dict__.items():
            if key[0] != '_':
                this_repr += f"{key} : {value}, "
        this_repr = sub(string=this_repr, pattern=", $", repl=")")
        return this_repr

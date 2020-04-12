from models import User
from hello import db
from sqlalchemy.exc import IntegrityError


def populate_users():
    """Reset users table and populate it."""
    User.__table__.drop(db.engine, checkfirst=True)
    User.__table__.create(db.engine, checkfirst=True)

    new_users = [
        {"name": "Logan", "code": "XMEN"},
        {"name": "Robert", "code": "RTX9"},
        {"name": "Emilie", "code": "AXRT"}
    ]

    for new_user in new_users:
        db.session.add(User(name=new_user['name'], code=new_user['code']))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

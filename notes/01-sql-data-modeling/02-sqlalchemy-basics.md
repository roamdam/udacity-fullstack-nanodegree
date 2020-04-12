SQLAlchemy basics
=================

# Layers of SQLAlchemy

| SQLAlchemy layer                | Abstraction level | Other libraries  | Behaviour                                |
|---------------------------------|-------------------|------------------|------------------------------------------|
| `connection_pool` and `dialect` | *none*            |                  |                                          |
| `engine`                        | DBAPI             | `psycopg2`       | send hand written SQL statements         |
| expressions                     | query builder     | `PyPika`         | build SQL statements from python objects |
| ORM                             | full ORM          | `pony`, `web2py` | map tables to classes                    |

![sqlalchemy-layers](../img/sqlalchemy-layers-of-abstraction.png)

# First flask app with SQLAlchemy

## Typical app structure

A main app file that will be run either with `flask run` or `python3 app.py`

```python
from hello import app
from models import User

@app.route('/')
def index():
    """Defines the landing page of the website."""
    first_user = User.query.first()
    return f"Hello {first_user.name} !"

if __name__ == '__main__':
    """So that app can be run with python3 app.py"""
    app.run()
```

`app` contains the flask application definition

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_uri = 'postgresql://romain@localhost:5432/gym'

app = Flask(import_name='Hello world')                  # this is the flask application/runner
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app=app)                                # this the ORM of the database
```

And `models.py` contains the schema of the database.

```python
from hello import db
# use db.create_all() to create those tables if they don't exist yet (not used here)

class User(db.Model):
    __tablename__ = "users"                         # overrides default lower caps from class name
    id = db.Column(db.Integer, primary_key=True)    # id being incremental is automatically guessed by SQLAlchemy
    name = db.Column(db.String, nullable=False)
```

## Basic operations

We reset a table then add records into it.

```python
from models import User
from hello import db
from sqlalchemy.exc import IntegrityError

def populate_users():
    """Reset users table and populate it."""
    User.__table__.drop(db.engine, checkfirst=True)    # drop only if exists
    User.__table__.create(db.engine, checkfirst=True)  # create only if exists

    new_users = [
        {"name": "Logan", "code": "XMEN"},
        {"name": "Robert", "code": None},              # will use the default value according to User's model
        {"name": "Emilie", "code": "AXRT"}
    ]

    for new_user in new_users:
        db.session.add(User(name=new_user['name'], code=new_user['code']))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
```
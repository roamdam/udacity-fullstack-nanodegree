from models import User
from hello import db

# Filter specifying the model
first_twos = User.query.filter(User.id < 3).all()
[print(user) for user in first_twos]

# Filter from within the table
xmen = User.query.filter_by(code='XMEN').all()
[print(user) for user in xmen]

# Case-sensitive, returns nothing
like_logan = User.query \
    .filter(
        User.name.like("%log%")
    ) \
    .first()

print(f'Here is case sensitive Logan : {like_logan}')

# Case insensitive, returns Logan
# table is queried using db.session
like_Logan = db.session.query(User) \
    .filter(
        User.name.ilike('%log%')
    ) \
    .first()

print(f"Here is case insensitive Logan : {like_Logan}")

from hello import app
from models import User
from populate import populate_users


populate_users()


@app.route('/')
def index():
    first_user = User.query.first()
    return f"Hello {first_user.name} !"


if __name__ == '__main__':
    app.run()

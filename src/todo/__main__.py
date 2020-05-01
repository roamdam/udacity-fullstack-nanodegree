from todo import app
from pyux import init_logger
from routes.index import index
from routes.create import create
from routes.clear import clear


if __name__ == '__main__':
    logger = init_logger()
    app.run()

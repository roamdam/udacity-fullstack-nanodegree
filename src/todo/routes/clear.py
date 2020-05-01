
from todo import app
from logging import getLogger
from flask import Response
from tasks.wiper import Wiper


@app.route('/todos/clear', methods=['POST'])
def clear():
    """POST request calling Wiper.clear() to delete all item records."""
    Wiper.clear()
    getLogger(__name__).info('Deleted all records from items table !')
    return Response(status=200)

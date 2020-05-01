from logging import getLogger

from flask import request, jsonify
from todo import app
from tasks.insert import ItemWriter


@app.route('/todos/create', methods=['POST'])
def create():
    """Use ItemWriter to insert a new row (POST request)."""
    logger = getLogger(__name__)
    content = request.get_json()
    ItemWriter.insert(data=content)
    logger.info(f'Added item from POST request {content}')
    return jsonify(**content)

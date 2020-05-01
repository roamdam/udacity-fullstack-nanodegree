from flask import render_template
from todo import app
from tasks.lister import ItemLister


@app.route('/')
def index():
    """Render the website html page, with all to do items."""
    page = render_template('index.html', data=ItemLister.get_all())
    return page

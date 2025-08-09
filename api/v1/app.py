#!/usr/bin/python3
""" create a flask application """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.teardown_appcontext
def closer(code):
    """closes a storage engine"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '0.0.0.0'
    app.run(host='0.0.0.0', port='5000', threaded=True)

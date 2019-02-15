import os

import flask
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.debug import DebuggedApplication

from InstagramAPI import InstagramAPI

USERNAME = os.getenv("INSTA_USERNAME")
PASSWORD = os.getenv("INSTA_PASSWORD")


def create_app(testing=False):
    app = flask.Flask(__name__)

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.url_map.strict_slashes = False

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app)

    API = InstagramAPI(USERNAME, PASSWORD)
    API.login()

    @app.route("/")
    def index():
        if API.tagFeed("malta"):
            json = API.LastJson["ranked_items"]

            return flask.render_template("index.html", images=json)
        return "ERROR"

    return app

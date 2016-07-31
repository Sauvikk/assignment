from werkzeug.wrappers import Request
from flask.ext.login import current_user
import flask


class SimpleMiddleWare(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(environ)
        print("something you want done in every http request")
        return self.app(environ, start_response)



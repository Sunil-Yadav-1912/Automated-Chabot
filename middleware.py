from werkzeug.wrappers import Request, Response
import sys
import config


class Middleware:

    def __init__(self, app):
        self.app = app
        self.client_id = config.CLIENT_ID
        self.client_secret = config.CLIENT_SECRET

    def __call__(self, environ, start_response):
        try:
            request = Request(environ)
            if request.path in config.BASIC_AUTH_ROUTES:
                if 'HTTP_X_CLIENT_ID' and 'HTTP_X_CLIENT_SECRET' in request.environ:
                    client_id = request.environ['HTTP_X_CLIENT_ID']
                    client_secret = request.environ['HTTP_X_CLIENT_SECRET']

                    if client_id == self.client_id and client_secret == self.client_secret:
                        return self.app(environ, start_response)

                res = Response('Authorization Failed', mimetype='text/plain', status=401)
                return res(environ, start_response)
            else:
                return self.app(environ, start_response)
        except Exception as ex:
            print("Exception: " + repr(ex), file=sys.stderr)
            res = Response('Authorization Failed', mimetype='text/plain', status=401)
            return res(environ, start_response)

from gevent import monkey

monkey.patch_all()

from app import app, launch_app
from core.config import TestSettings
from gevent.pywsgi import WSGIServer

settings = TestSettings()

http_server = WSGIServer(('', settings.SERVICE_PORT), launch_app(app))
http_server.serve_forever()

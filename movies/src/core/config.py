import logging
import os
from logging import config as logging_config

from core.logger import LOGGING

logging.basicConfig(filename="project.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger('log')
logging_config.dictConfig(LOGGING)


PROJECT_NAME = os.getenv('FasterAPI', 'Movies Service')

REDIS_HOST = os.getenv('REDIS_HOST', 'redis-test')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'elastic')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

AUTH_SERVICE_HOST = os.getenv('AUTH_SERVICE_HOST', 'api')
AUTH_SERVICE_PORT = int(os.getenv('AUTH_SERVICE_PORT', 5000))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

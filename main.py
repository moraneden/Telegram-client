import logging.config
import os
from client import *

try:
    if not os.path.exists('logs'):
        os.makedirs('logs')
    if not os.path.exists('temp'):
        os.makedirs('temp')
except OSError as e:
    raise

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    try:
        client = TgClient()
        client.run()
    except Exception as e:
        logging.exception('General error: ' + str(e))


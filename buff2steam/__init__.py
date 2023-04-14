import json
import os
import pathlib
import sys

import loguru

base_path = pathlib.Path(os.path.abspath(__file__)).parent.parent
config_path = os.path.join(base_path, 'config.json')

config = json.load(open(config_path))

logger = loguru.logger
logger.remove()
logger.add(os.path.join(base_path, 'buff2steam.log'), level='DEBUG' if config['main']['debug'] else 'INFO')
logger.add(sys.stdout, level='DEBUG' if config['main']['debug'] else 'INFO')

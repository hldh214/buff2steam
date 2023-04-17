import json
import os
import pathlib
import sys

import loguru

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # https://pyinstaller.org/en/stable/runtime-information.html
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    base_path = sys._MEIPASS  # noqa
else:
    base_path = pathlib.Path(os.path.abspath(__file__)).parent.parent

config_path = os.path.join(base_path, 'config.json')

config = json.load(open(config_path))

logger = loguru.logger
logger.remove()
logger.add(os.path.join(base_path, 'buff2steam.log'), level='DEBUG' if config['main']['debug'] else 'INFO')
logger.add(sys.stdout, level='DEBUG' if config['main']['debug'] else 'INFO')

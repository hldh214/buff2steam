import json
import re
import typing

import requests

from http.cookies import SimpleCookie

from requests.cookies import cookiejar_from_dict

__all__ = ['requests', 'typing', 'BaseProvider', 'json', 're', 'SimpleCookie', 'cookiejar_from_dict']


class BaseProvider():
    def __init__(self, opener=None):
        """
        :type opener: requests.Session
        """
        self.opener = opener if opener else requests.session()

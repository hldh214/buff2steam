import typing

import requests

__all__ = ['requests', 'typing', 'BaseProvider']


class BaseProvider():
    def __init__(self, opener=None):
        """
        :type opener: requests.Session
        """
        self.opener = opener if opener else requests.session()

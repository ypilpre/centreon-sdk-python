# -*- coding: utf-8 -*-

from centreonapi.webservice import Webservice


class CentreonDecorator(object):

    @staticmethod
    def post_refresh(func):
        """
        Decorator that call __refresh_list() after func unless
        function's call contains 'post_refresh=False'
        eg:
            @post_refresh
            def hello(w, post_refresh=False):
                ...
        """
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # args[0] is always self
            # https://coderwall.com/p/jo39na/python-decorators-using-self
            if kwargs.get("post_refresh", True):
                args[0]._refresh_list()
            return result
        return wrapper

    @staticmethod
    def pre_refresh(func):
        def wrapper(*args, **kwargs):
            args[0]._refresh_list()
            return func(*args, **kwargs)
        return wrapper

    def _refresh_list(self):
        pass


class CentreonClass(object):

    def __init__(self):
        self.webservice = Webservice.getInstance()

    def get(self, name):
        return self[name]

    def exists(self, name):
        return name in self

    def list(self):
        pass


class CentreonObject(object):

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
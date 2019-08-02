# -*- coding: utf-8 -*-

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class Webservice(object):
    """
    Class for call Centreon Web Rest webservices
    """

    __instance = None

    def __new__(cls):
        """
        Constructor with singleton for webservices
        """
        if Webservice.__instance is None:
            Webservice.__instance = object.__new__(cls)
            Webservice.__instance.url = None
            Webservice.__instance.authuser = None
            Webservice.__instance.authpass = None
            Webservice.__instance.auth_token = None
            Webservice.__instance.check_ssl = True
        return Webservice.__instance

    def load(self, url, username, password, check_ssl=True):
        """
        Load configuration for webservices

        :param url: The Centreon Web URL
        :type url: String
        :param username: The username for connect to Centreon Web webservices
        :type username: String
        :param password: The password for connect to Centreon Web webservices
        :type password: String
        """
        self.url = url
        self.authuser = username
        self.authpass = password
        self.check_ssl = check_ssl

    def isLoaded(self):
        """
        Test if webservices configuration is loaded

        :return: If the webservices configuration is loaded
        :rtype: Boolean
        """
        if self.url is None:
            return False
        return True

    def auth(self):
        """
        Authenticate to the webservices
        """
        request = requests.post(
            self.url + '/api/index.php?action=authenticate',
            data={
                'username': self.authuser,
                'password': self.authpass
            },
            verify=self.check_ssl
        )
        request.raise_for_status()
        data = request.json()
        self.auth_token = data['authToken']

    def call_clapi(self, action=None, obj=None, values=None):
        """
        Call an endpoint of Centreon Web for clapi wrapper

        :param action: The clapi action
        :type action: String
        :param obj: The clapi object
        :type obj: String
        :param values: The values for the call
        :type values: mixed
        :return: The response of call
        :rtype: dict
        """
        if self.auth_token is None:
            self.auth()

        data = {}

        if action is not None:
            data['action'] = action
        if obj is not None:
            data['object'] = obj
        if values is not None:
            data['values'] = values

        request = requests.post(
            self.url + '/api/index.php?action=action&object=centreon_clapi',
            headers={'centreon-auth-token': self.auth_token},
            json=data,
            verify=self.check_ssl
        )
        request.raise_for_status()
        return request.json()

    def centreon_realtime(self, action=None, obj=None, values=None):
        if self.auth_token is None:
            self.auth()

        data = {}
        obj_supported = ('hosts', 'services')

        if action is not None:
            data['action'] = action
        if obj is not None:
            if obj in obj_supported:
                data['object'] = obj
            else:
                raise ValueError("Only support <hosts> or <services>")

        if not self.check_ssl:
            # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            requests.packages.urllib3\
                .disable_warnings(InsecureRequestWarning)

        request = requests.get(
            self.url + '/api/index.php?object=centreon_realtime_'
                     + obj + '&action=' + action,
            headers={
                'Content-Type': 'application/json',
                'centreon-auth-token': self.auth_token
            },
            params=values,
            verify=self.check_ssl
        )
        request.raise_for_status()
        return request.json()

    @staticmethod
    def getInstance(url=None, username=None, password=None, check_ssl=True):
        """
        Get an unique instance of the webservices

        :param url: The Centreon Web URL
        :type url: String
        :param username: The username for connect to Centreon Web webservices
        :type username: String
        :param password: The password for connect to Centreon Web webservices
        :type password: String
        """
        instance = Webservice()
        if instance.isLoaded():
            return instance
        if url is None or username is None or password is None:
            raise KeyError('Missing parameters to load the Webservice')
        instance.load(url, username, password, check_ssl)
        return instance

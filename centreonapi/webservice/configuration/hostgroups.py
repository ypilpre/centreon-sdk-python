# -*- coding: utf-8 -*-

from centreonapi.webservice import Webservice

class Hostgroups(object):

    def __init__(self):
        """
        Constructor
        """
        self.webservice = Webservice.getInstance()

    def list(self):
        """
        Get HostGroups list
        """
        return self.webservice.call_clapi('show', 'HG')


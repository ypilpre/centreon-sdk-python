# -*- coding: utf-8 -*-

from centreonapi.webservice import Webservice

class Poller(object):
    """
    Centreon Web poller
    """

    def __init__(self):
        """
        Constructor
        """
        self.webservice = Webservice.getInstance()

    def applycfg(self, pollername):
        """
        Apply the configuration to a poller name
        """
        return self.webservice.call_clapi('applycfg', None, pollername)

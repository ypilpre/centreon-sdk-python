# -*- coding: utf-8 -*-

from centreonapi.webservice import Webservice

class Host(object):
    """
    Centreon Web host object
    """

    def __init__(self):
        """
        Constructor
        """
        self.webservice = Webservice.getInstance()

    def list(self):
        """
        List hosts
        """
        return self.webservice.call_clapi('show', 'HOST')

    def add(self, hostname, hostalias, hostip, hosttemplate, pollername, hgname):
        """
        Add a host
        """
        values = [
            hostname,
            hostalias,
            hostip,
            hosttemplate,
            pollername,
            hgname
        ]
        return self.webservice.call_clapi('add', 'HOST', values)

    def applytpl(self, hostname):
        """
        Apply the host template to the host, deploy services
        """
        return self.webservice.call_clapi('applytpl', 'HOST', hostname)

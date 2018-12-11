# -*- coding: utf-8 -*-

from centreonapi.webservice.configuration.common import *
from overrides import overrides


class Poller(CentreonObject):

    def __init__(self, properties):
        self.id = properties['id']
        self.bin = properties['bin']
        self.activate = properties['activate']
        self.init_script = properties['init script']
        self.ipaddress = properties['ip address']
        self.localhost = properties['localhost']
        self.name = properties['name']
        self.ssh_port = properties['ssh port']
        self.stats_bin = properties['stats bin']
        self.status = properties['status']
        self.pollerHost = dict()

    def add(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def setparam(self, *args, **kwargs):
        pass

    def gethosts(self):
        for poller in self.webservice.call_clapi('gethosts', 'INSTANCE', self.name)['result']:
            poller['poller'] = poller.name
            pollerhost_obj = PollerHost(poller)
            self.pollerHost[pollerhost_obj.name] = pollerhost_obj
        return self.pollerHost


class PollerHost(CentreonObject):

    def __init__(self, properties):
        self.id = properties['id']
        self.address = properties['address']
        self.name = properties['name']
        self.poller = properties['poller']


class Pollers(CentreonDecorator, CentreonClass):
    """
    Centreon Web poller
    """

    def __init__(self):
        super(Pollers, self).__init__()
        self.pollers = dict()

    def __contains__(self, name):
        return name in self.pollers.keys()

    def __getitem__(self, name):
        if not self.pollers:
            self.list()
        if name in self.pollers.keys():
            return self.pollers[name]
        else:
            raise ValueError("Instance %s not found" % name)

    @overrides
    def _refresh_list(self):
        self.pollers.clear()
        for poller in self.webservice.call_clapi('show', 'INSTANCE')['result']:
            poller_obj = Poller(poller)
            self.pollers[poller_obj.name] = poller_obj

    def applycfg(self, pollername):
        """
        Apply the configuration to a poller name
        """
        return self.webservice.call_clapi('applycfg', None, pollername)

    @CentreonDecorator.pre_refresh
    def list(self):
        return self.pollers



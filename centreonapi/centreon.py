# -*- coding: utf-8 -*-

from centreonapi.webservice.configuration.host import *
from centreonapi.webservice.configuration.service import Service
from centreonapi.webservice.configuration.poller import Pollers
from centreonapi.webservice.configuration.hostgroups import HostGroups
from centreonapi.webservice.configuration.templates import HostTemplates
from centreonapi.webservice.configuration.command import Command
from centreonapi.webservice.configuration.resourcecfg import ResourceCFG


class Centreon(object):

    def __init__(self, url=None, username=None, password=None, check_ssl=True):
        Webservice.getInstance(
            url,
            username,
            password,
            check_ssl
        )

        self.hosts = Hosts()
        self.services = Service()
        self.pollers = Pollers()
        self.hostgroups = HostGroups()
        self.hosttemplates = HostTemplates()
        self.commands = Command()
        self.resourcecfgs = ResourceCFG()

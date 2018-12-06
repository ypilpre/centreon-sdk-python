# -*- coding: utf-8 -*-

from centreonapi.webservice.configuration.common import *


class HostGroup(CentreonObject):

    def __init__(self, properties):
        self.id = properties['id']
        self.alias = properties['alias']
        self.name = properties['name']


class HostGroups(CentreonDecorator, CentreonClass):

    def __init__(self):
        super(HostGroups, self).__init__()
        self.hostgroups = dict()

    def __contains__(self, name):
        return name in self.hostgroups.keys()

    def __getitem__(self, name):
        if not self.hostgroups:
            self.list()
        if name in self.hostgroups.keys():
            return self.hostgroups[name]
        else:
            raise ValueError("Hostgroup %s not found" % name)

    def _refresh_list(self):
        self.hostgroups.clear()
        for hg in self.webservice.call_clapi('show', 'HG')['result']:
            hg_obj = HostGroup(hg)
            self.hostgroups[hg_obj.name] = hg_obj

    @CentreonDecorator.pre_refresh
    def list(self):
        return self.hostgroups

    @CentreonDecorator.post_refresh
    def add(self, name, alias):
        values = [ name, alias]
        return self.webservice.call_clapi('add', 'HG', values)

    @CentreonDecorator.post_refresh
    def delete(self, name):
        return self.webservice.call_clapi('del', 'HG', name)



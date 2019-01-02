# -*- coding: utf-8 -*-

import centreonapi.webservice.configuration.common as common


class HostGroup(common.CentreonObject):

    def __init__(self, properties):
        self.id = properties.get('id')
        self.alias = properties.get('alias')
        self.name = properties.get('name')


class HostGroups(common.CentreonDecorator, common.CentreonClass):

    def __init__(self):
        super(HostGroups, self).__init__()
        self.hostgroups = dict()
        self.__clapi_action = 'HG'

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
        for hg in self.webservice.call_clapi(
                'show',
                self.__clapi_action)['result']:
            hg_obj = HostGroup(hg)
            self.hostgroups[hg_obj.name] = hg_obj

    @common.CentreonDecorator.pre_refresh
    def list(self):
        return self.hostgroups

    @common.CentreonDecorator.post_refresh
    def add(self, name, alias):
        values = [name, alias]
        return self.webservice.call_clapi('add', self.__clapi_action, values)

    @common.CentreonDecorator.post_refresh
    def delete(self, name):
        return self.webservice.call_clapi('del', self.__clapi_action, name)

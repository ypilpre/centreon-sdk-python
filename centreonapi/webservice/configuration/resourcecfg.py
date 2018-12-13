# -*- coding: utf-8 -*-

from centreonapi.webservice.configuration.common import *
from centreonapi.webservice.configuration.poller import Poller


class ResourceCFG(CentreonObject):

    def __init__(self, properties):
        self.webservice = Webservice.getInstance()
        self.id = properties.get('id')
        self.instance = properties.get('instance')
        self.name = properties.get('name')
        self.activate = properties.get('activate')
        self.value = properties.get('value')

    def setparam(self, name, value):
        values = [
            self.id,
            name,
            value
        ]
        return self.webservice.call_clapi('setparam', 'RESOURCECFG', values)


class ResourceCFGs(CentreonDecorator, CentreonClass):
    """
    Centreon Web Resource object
    """
    def __init__(self):
        super(ResourceCFGs, self).__init__()
        self.resources = dict()

    @staticmethod
    def _build_resource_line(line):
        if line:
            rsc = line
            if rsc[0] != '$':
                rsc = '$' + rsc
            if rsc[len(rsc) - 1] != '$':
                rsc = rsc + '$'
            return str(rsc)
        else:
            return ""

    def __contains__(self, name):
        rsc = self._build_resource_line(name)
        return rsc in self.resources.keys()

    def __getitem__(self, name):
        if not self.resources:
            self.list()
        rsc = self._build_resource_line(name)
        if rsc in self.resources.keys():
            return self.resources[rsc]
        else:
            raise ValueError("Resource %s not found" % rsc)

    def _refresh_list(self):
        self.resources.clear()
        for resource in self.webservice.call_clapi('show', 'RESOURCECFG')['result']:
            resource_obj = ResourceCFG(resource)
            self.resources[resource_obj.name] = resource_obj

    @CentreonDecorator.pre_refresh
    def list(self):
        return self.resources

    @CentreonDecorator.post_refresh
    def add(self, rscname, rscvalue, rscinstance, rsccomment, post_refresh=True):
        values = [
            rscname,
            rscvalue,
            str(self._build_param(rscinstance, Poller)[0]),
            rsccomment
        ]
        return self.webservice.call_clapi('add', 'RESOURCECFG', values)

    @CentreonDecorator.post_refresh
    def delete(self, resource, post_refresh=True):
        value = str(self._build_param(resource, ResourceCFG, attr='id')[0])
        return self.webservice.call_clapi('del', 'RESOURCECFG', value)

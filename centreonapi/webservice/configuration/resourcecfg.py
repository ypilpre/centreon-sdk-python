# -*- coding: utf-8 -*-

from centreonapi.webservice.configuration.common import *
from overrides import overrides


class ResourceCFGObj(CentreonObject):

    def __init__(self, properties):
        self.id = properties['id']
        self.instance = properties['instance']
        self.name = properties['name']
        self.activate = properties['activate']
        self.value = properties['value']


class ResourceCFG(CentreonDecorator, CentreonClass):
    """
    Centreon Web Resource object
    """
    def __init__(self):
        super(ResourceCFG, self).__init__()
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

    @overrides
    def _refresh_list(self):
        self.resources.clear()
        for resource in self.webservice.call_clapi('show', 'RESOURCECFG')['result']:
            resource_obj = ResourceCFGObj(resource)
            self.resources[resource_obj.name] = resource_obj

    @CentreonDecorator.pre_refresh
    def list(self):
        return self.resources

    @CentreonDecorator.post_refresh
    def add(self, rscname, rscvalue, rscinstance, rsccomment, post_refresh=True):
        values = [
            rscname,
            rscvalue,
            rscinstance,
            rsccomment
        ]
        return self.webservice.call_clapi('add', 'RESOURCECFG', values)

    @CentreonDecorator.post_refresh
    def delete(self, resource, post_refresh=True):
        if not resource:
            raise ValueError("Resource is empty")
        return self.webservice.call_clapi('del', 'RESOURCECFG', resource.id)

    @CentreonDecorator.post_refresh
    def setparam(self, resource, name, value, post_refresh=True):
        values = [
            resource.id,
            name,
            value
        ]
        return self.webservice.call_clapi('setparam', 'RESOURCECFG', values)

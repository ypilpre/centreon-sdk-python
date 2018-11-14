# -*- coding: utf-8 -*-

from centreonapi.webservice import Webservice

class ResourceCFGObj(object):

    def __init__(self, properties):
        self.id = properties['id']
        self.instance = properties['instance']
        self.name = properties['name']
        self.activate = properties['activate']
        self.value = properties['value']

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class ResourceCFG(object):
    """
    Centreon Web Resource object
    """

    def __init__(self):
        """
        Constructor
        """
        self.webservice = Webservice.getInstance()
        self.resources = dict()

    def list(self):
        """
        List resource
        """
        self.resources.clear()
        for resource in self.webservice.call_clapi('show', 'RESOURCECFG')['result']:
            resource_obj = ResourceCFGObj(resource)
            self.resources[resource_obj.name] = resource_obj
        return self.resources

    def add(self, rscname, rscvalue, rscinstance, rsccomment):
        """
        add new resource
        """
        values = [
            rscname,
            rscvalue,
            rscinstance,
            rsccomment
        ]
        return self.webservice.call_clapi('add', 'RESOURCECFG', values)

    def delete(self, rscid):
        """
        Delete a command
        """
        return self.webservice.call_clapi('del', 'RESOURCECFG', rscid)

    def setparam(self, rscid, name, value):
        """
        SetParam on command
        """
        values = [
            rscid,
            name,
            value
        ]
        return self.webservice.call_clapi('setparam', 'RESOURCECFG', values)

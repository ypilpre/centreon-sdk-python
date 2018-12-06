# -*- coding: utf-8 -*-

from centreonapi.webservice.configuration.common import *


class HostTemplate(CentreonObject):

    def __init__(self, properties):
        self.id = properties.get('id')
        self.name = properties.get('name')
        self.activate = properties.get('activate')
        self.alias =  properties.get('alias')
        self.address = properties.get('address')


class HostTemplates(CentreonDecorator, CentreonClass):

    def __init__(self):
        super(HostTemplates, self).__init__()
        self.hosttemplates = dict()

    def __contains__(self, name):
        return name in self.hosttemplates.keys()

    def __getitem__(self, name):
        if not self.hosttemplates:
            self.list()
        if name in self.hosttemplates.keys():
            return self.hosttemplates[name]
        else:
            raise ValueError("HostTemplates %s not found" % name)

    def _refresh_list(self):
        self.hosttemplates.clear()
        for htpl in self.webservice.call_clapi('show', 'HTPL')['result']:
            htpl_obj = HostTemplate(htpl)
            self.hosttemplates[htpl_obj.name] = htpl_obj

    @CentreonDecorator.pre_refresh
    def list(self):
        return self.hosttemplates



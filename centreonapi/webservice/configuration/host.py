# -*- coding: utf-8 -*-

import centreonapi.webservice.configuration.common as common
from centreonapi.webservice.configuration.poller import Poller
from centreonapi.webservice.configuration.hostgroups import HostGroup
from centreonapi.webservice.configuration.contact import ContactGroup, Contact
from centreonapi.webservice import Webservice


class Host(common.CentreonObject):

    def __init__(self, properties):
        self.webservice = Webservice.getInstance()
        self.__clapi_action = 'HOST'
        self.id = properties.get('id')
        self.name = properties.get('name')
        self.state = properties.get('activate')
        self.address = properties.get('address')
        self.alias = properties.get('alias')
        self.macros = dict()
        self.templates = dict()
        self.parents = dict()
        self.hostgroups = dict()
        self.contactgroups = dict()
        self.contacts = dict()
        self.state = properties.get('state')

    def getmacro(self):
        self.macros.clear()
        for macro in self.webservice.call_clapi(
                'getmacro',
                self.__clapi_action,
                self.name)['result']:
            macro_obj = HostMacro(macro)
            self.macros[macro_obj.name] = macro_obj
        return self.macros

    def setmacro(self, name, value):
        values = [self.name, name, value]
        return self.webservice.call_clapi(
            'setmacro',
            self.__clapi_action,
            values)

    def deletemacro(self, macro):
        values = [self.name,
                  "|".join(common.build_param(macro, HostMacro))]
        return self.webservice.call_clapi(
            'delmacro',
            self.__clapi_action,
            values)

    def gettemplate(self):
        for template in self.webservice.call_clapi(
                'gettemplate',
                self.__clapi_action,
                self.name)['result']:
            template_obj = HostTemplate(template)
            self.templates[template_obj.id] = template_obj
        return self.templates

    def settemplate(self, template=None):
        values = [self.name,
                  "|".join(common.build_param(template, HostTemplate))]
        return self.webservice.call_clapi(
            'settemplate',
            self.__clapi_action,
            values)

    def addtemplate(self, template=None):
        values = [self.name,
                  "|".join(common.build_param(template, HostTemplate))]
        return self.webservice.call_clapi(
            'addtemplate',
            self.__clapi_action,
            values)

    def deletetemplate(self, template=None):
        values = [self.name,
                  str("|".join(common.build_param(template, HostTemplate)))]
        return self.webservice.call_clapi(
            'deltemplate',
            self.__clapi_action,
            values)

    def applytemplate(self):
        return self.webservice.call_clapi(
            'applytpl',
            self.__clapi_action,
            self.name)

    def enable(self):
        return self.webservice.call_clapi(
            'enable',
            self.__clapi_action,
            self.name)

    def disable(self):
        return self.webservice.call_clapi(
            'disable',
            self.__clapi_action,
            self.name)

    def setinstance(self, instance):
        values = [self.name,
                  str(common.build_param(instance, Poller)[0])]
        return self.webservice.call_clapi(
            'setinstance',
            self.__clapi_action,
            values)

    def status(self):
        values = {'search': self.name}
        self.state = self.webservice.centreon_realtime(
            'list',
             'hosts',
            values)[0]['state']
        return self.state

    def getparent(self):
        for parent in self.webservice.call_clapi(
                'getparent',
                self.__clapi_action,
                self.name)['result']:
            parent_obj = HostParent(parent)
            self.parents[parent_obj.name] = parent_obj
        return self.parents

    def addparent(self, parents):
        values = [self.name,
                  "|".join(common.build_param(parents, HostParent))]
        return self.webservice.call_clapi(
            'addparent',
            self.__clapi_action,
            values)

    def setparent(self, parents):
        values = [self.name,
                  "|".join(common.build_param(parents, HostParent))]
        return self.webservice.call_clapi(
            'setparent',
            self.__clapi_action,
            values)

    def deleteparent(self, parents):
        values = [self.name,
                  "|".join(common.build_param(parents, HostParent))]
        return self.webservice.call_clapi(
            'delparent',
            self.__clapi_action,
            values)

    def gethostgroup(self):
        for hgs in  self.webservice.call_clapi(
                'gethostgroup',
                self.__clapi_action,
                self.name)['result']:
            hg_obj = HostGroup(hgs)
            self.hostgroups[hg_obj.name] = hg_obj
        return self.hostgroups

    def addhostgroup(self, hostgroup=None):
        values = [self.name,
                  "|".join(common.build_param(hostgroup, HostGroup))]
        return self.webservice.call_clapi(
            'addhostgroup',
            self.__clapi_action,
            values)

    def sethostgroup(self, hostgroup=None):
        values = [self.name,
                  "|".join(common.build_param(hostgroup, HostGroup))]
        return self.webservice.call_clapi(
            'sethostgroup',
            self.__clapi_action,
            values)

    def deletehostgroup(self, hostgroup=None):
        values = [self.name,
                  "|".join(common.build_param(hostgroup, HostGroup))]
        return self.webservice.call_clapi(
            'delhostgroup',
            self.__clapi_action,
            values)

    def getcontactgroup(self):
        for cgs in self.webservice.call_clapi(
                'getcontactgroup',
                self.__clapi_action,
                self.name)['result']:
            cg_obj = ContactGroup(cgs)
            self.contactgroups[cg_obj.name] = cg_obj
        return self.contactgroups

    def addcontactgroup(self, contactgroups):
        values = [self.name,
                  "|".join(common.build_param(contactgroups, ContactGroup))]
        return self.webservice.call_clapi(
            'addcontactgroup',
            self.__clapi_action,
            values)

    def setcontactgroup(self, contactgroups):
        values = [self.name,
                  "|".join(common.build_param(contactgroups, ContactGroup))]
        return self.webservice.call_clapi(
            'setcontactgroup',
            self.__clapi_action,
            values)

    def deletecontactgroup(self, contactgroups):
        values = [self.name,
                  "|".join(common.build_param(contactgroups, ContactGroup))]
        return self.webservice.call_clapi(
            'delcontactgroup',
            self.__clapi_action,
            values)

    def getcontact(self):
        for cs in self.webservice.call_clapi(
                'getcontact',
                self.__clapi_action,
                self.name)['result']:
            c_obj = Contact(cs)
            self.contacts[c_obj.name] = c_obj
        return self.contacts

    def addcontact(self, contacts):
        values = [self.name,
                  "|".join(common.build_param(contacts, Contact))]
        return self.webservice.call_clapi(
            'addcontact',
             self.__clapi_action,
            values)

    def setcontact(self, contacts):
        values = [self.name,
                  "|".join(common.build_param(contacts, Contact))]
        return self.webservice.call_clapi(
            'setcontact',
             self.__clapi_action,
             values)

    def deletecontact(self, contacts):
        values = [self.name,
                  "|".join(common.build_param(contacts, Contact))]
        return self.webservice.call_clapi(
            'delcontact',
            self.__clapi_action,
            values)

    def setseverity(self, name):
        pass
        #return self.webservice.call_clapi(
        #    'setseverity',
        #    self.__clapi_action,
        #    [self.name, name])

    def unsetseverity(self):
        pass
        #return self.webservice.call_clapi(
        #    'unsetseverity',
        #    self.__clapi_action,
        #    self.name)

    def setparam(self, name, value):
        values = [self.name, name, value]
        return self.webservice.call_clapi(
            'setparam',
            self.__clapi_action,
            values)

    def getparam(self, name):
        pass


class HostMacro(common.CentreonObject):

    def __init__(self, properties):
        self.name = properties.get('macro name')
        self.value = properties.get('macro value')
        self.description = properties.get('description')
        self.is_password = properties.get('is_password')
        self.source = properties.get('source')

    def __repr__(self):
        return self.name + ' / ' + self.value

    def __str__(self):
        return self.name + ' / ' + self.value


class HostParent(common.CentreonObject):

    def __init__(self, properties):
        self.name = properties.get('name')
        self.id = properties.get('id')


class Hosts(common.CentreonDecorator, common.CentreonClass):
    """
    Centreon Web host object
    """

    def __init__(self):
        super(Hosts, self).__init__()
        self.hosts = dict()
        self.__clapi_action = 'HOST'

    def __contains__(self, name):
        return name in self.hosts.keys()

    def __getitem__(self, name):
        if not self.hosts:
            self.list()
        if name in self.hosts.keys():
            return self.hosts[name]
        else:
            raise ValueError("Host %s not found" % name)

    def _refresh_list(self):
        self.hosts = dict()
        for host in self.webservice.call_clapi(
                'show',
                self.__clapi_action)['result']:
            host_obj = Host(host)
            self.hosts[host_obj.name] = host_obj

    @common.CentreonDecorator.pre_refresh
    def list(self):
        return self.hosts

    @common.CentreonDecorator.post_refresh
    def add(self,
            name,
            alias,
            ip,
            instance=None,
            template=None,
            hg=None,
            post_refresh=True):
        """
        Add new Host on Centreon platform
        :param name: name for host
        :param alias:  alias (short name for example)
        :param ip: Ip address or DNS
        :param instance: Poller() or str()
        :param template: HostTemplate(), list() of HostTemplate(),
         list() of str() or str()
        :param hg: HostGroup(), list() of HostGroup(),
         list() of str() or str()
        :return:
        """
        values = [
            name,
            alias,
            ip,
            str("|".join(common.build_param(template, HostTemplate))),
            str(common.build_param(instance, Poller)[0]),
            str("|".join(common.build_param(hg, HostGroup)))
        ]
        return self.webservice.call_clapi(
            'add',
            self.__clapi_action,
            values)

    @common.CentreonDecorator.post_refresh
    def delete(self, host, post_refresh=True):
        value = str(common.build_param(host, Hosts)[0])
        return self.webservice.call_clapi(
            'del',
            self.__clapi_action,
            value)


class HostTemplates(Hosts):
    def __init__(self):
        super(HostTemplates, self).__init__()
        self.__clapi_action = 'HTPL'


class HostTemplate(Host):

    def __init__(self, properties):
        super(HostTemplate, self).__init__(properties)
        self.__clapi_action = 'HTPL'

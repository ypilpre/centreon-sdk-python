# -*- coding: utf-8 -*-

from centreonapi.webservice.configuration.common import *
from centreonapi.webservice.configuration.templates import HostTemplate
from centreonapi.webservice.configuration.poller import Poller
from centreonapi.webservice.configuration.hostgroups import HostGroup


class Host(CentreonObject):

    def __init__(self, properties):
        self.webservice = Webservice.getInstance()
        self.id = properties.get('id')
        self.name = properties.get('name')
        self.state = properties.get('activate')
        self.address = properties.get('address')
        self.alias = properties.get('alias')
        self.macros = dict()
        self.templates = dict()
        self.state = properties.get('state')

    def getmacro(self):
        self.macros.clear()
        for macro in self.webservice.call_clapi('getmacro', 'HOST', self.name)['result']:
            macro_obj = HostMacro(macro)
            self.macros[macro_obj.name] = macro_obj
        return self.macros

    def setmacro(self, name, value):
        values = [self.name, name, value]
        return self.webservice.call_clapi('setmacro', 'HOST', values)

    def deletemacro(self, name):
        values = [self.name, name]
        return self.webservice.call_clapi('delmacro', 'HOST', values)

    @staticmethod
    def __build_template(template=None):
        if template and isinstance(template, HostTemplate):
            _template = "|".join(template.name)
        elif template and isinstance(template, list):
            tmp_hosttmpl = list()
            for htmpl in template:
                tmp_hosttmpl.append(htmpl.name)
            _template = "|".join(tmp_hosttmpl)
        elif template and isinstance(template, str):
            _template = template
        else:
            raise ValueError("HostTemplate must be defined")
        return _template

    @staticmethod
    def __build_hostgroup(hg=None):
        if hg and isinstance(hg, HostGroup):
            _hg = "|".join(hg.name)
        elif hg and isinstance(hg, list):
            tmp_hg = list()
            for hgobj in hg:
                tmp_hg.append(hgobj.name)
            _hg = "|".join(tmp_hg)
        elif hg and isinstance(hg, str):
            _hg = hg
        else:
            raise ValueError("HostGroup must be defined")
        return _hg

    def gettemplate(self):
        for template in self.webservice.call_clapi('gettemplate', 'HOST', self.name)['result']:
            template_obj = HostTemplate(template)
            self.templates[template_obj.id] = template_obj
        return self.templates

    def settemplate(self, template=None):
        values = [self.name, self.__build_template(template)]
        return self.webservice.call_clapi('settemplate', 'HOST', values)

    def addtemplate(self, template=None):
        values = [self.name, self.__build_template(template)]
        return self.webservice.call_clapi('addtemplate', 'HOST', values)

    def deletetemplate(self, template=None):
        values = [self.name, self.__build_template(template)]
        return self.webservice.call_clapi('delemplate', 'HOST', values)

    def applytemplate(self):
        return self.webservice.call_clapi('applytpl', 'HOST', self.name)

    def enable(self):
        return self.webservice.call_clapi('enable', 'HOST', self.name)

    def disable(self):
        return self.webservice.call_clapi('disable', 'HOST', self.name)

    def setinstance(self, instance):
        values = [self.name, instance]
        return self.webservice.call_clapi('setinstance', 'HOST', values)

    def status(self):
        values = {'search': self.name}
        self.state = self.webservice.centreon_realtime('list', 'hosts', values)[0]['state']
        return self.state

    def getparent(self):
        return self.webservice.call_clapi('getparent', 'HOST', self.name)

    def addparent(self, parents):
        return self.webservice.call_clapi('addparent', 'HOST', [self.name, "|".join(parents)])

    def setparent(self, parents):
        return self.webservice.call_clapi('setparent', 'HOST', [self.name, "|".join(parents)])

    def deleteparent(self, parents):
        return self.webservice.call_clapi('delparent', 'HOST', [self.name, "|".join(parents)])

    def gethostgroup(self):
        return self.webservice.call_clapi('gethostgroup', 'HOST', self.name)

    def addhostgroup(self, hostgroup=None):
        values = [self.name, self.__build_hostgroup(hostgroup)]
        return self.webservice.call_clapi('addhostgroup', 'HOST', values)

    def sethostgroup(self, hostgroup=None):
        values = [self.name, self.__build_hostgroup(hostgroup)]
        return self.webservice.call_clapi('sethostgroup', 'HOST', values)

    def deletehostgroup(self, hostgroup=None):
        values = [self.name, self.__build_hostgroup(hostgroup)]
        return self.webservice.call_clapi('delhostgroup', 'HOST', values)

    def getcontactgroup(self):
        return self.webservice.call_clapi('getcontactgroup', 'HOST', self.name)

    def addcontactgroup(self, contactgroups):
        return self.webservice.call_clapi('addcontactgroup', 'HOST', [self.name, "|".join(contactgroups)])

    def setcontactgroup(self, contactgroups):
        return self.webservice.call_clapi('setcontactgroup', 'HOST', [self.name, "|".join(contactgroups)])

    def deletecontactgroup(self, contactgroups):
        return self.webservice.call_clapi('delcontactgroup', 'HOST', [self.name, "|".join(contactgroups)])

    def getcontact(self):
        return self.webservice.call_clapi('getcontact', 'HOST', self.name)

    def addcontact(self, contacts):
        return self.webservice.call_clapi('addcontact', 'HOST', [self.name, "|".join(contacts)])

    def setcontact(self, contacts):
        return self.webservice.call_clapi('setcontact', 'HOST', [self.name, "|".join(contacts)])

    def deletecontact(self, contacts):
        return self.webservice.call_clapi('delcontact', 'HOST', [self.name, "|".join(contacts)])

    def setseverity(self, name):
        return self.webservice.call_clapi('setseverity', 'HOST', [self.name, name])

    def unsetseverity(self):
        return self.webservice.call_clapi('unsetseverity', 'HOST', self.name)


class HostMacro(CentreonObject):

    def __init__(self, properties):
        self.name = properties['macro name']
        self.value = properties['macro value']
        self.description = properties['description']
        self.is_password = properties['is_password']
        self.source = properties['source']

    def __repr__(self):
        return self.name + ' / ' + self.value

    def __str__(self):
        return self.name + ' / ' + self.value


class Hosts(CentreonDecorator, CentreonClass):
    """
    Centreon Web host object
    """

    def __init__(self):
        super(Hosts, self).__init__()
        self.hosts = dict()

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
        for host in self.webservice.call_clapi('show', 'HOST')['result']:
            host_obj = Host(host)
            self.hosts[host_obj.name] = host_obj

    @CentreonDecorator.pre_refresh
    def list(self):
        return self.hosts

    @CentreonDecorator.post_refresh
    def add(self, name, alias, ip, instance, template=None, hg=None):
        """
        Add new Host on Centreon platform
        :param name: name for host
        :param alias:  alias (short name for example)
        :param ip: Ip address or DNS
        :param instance: Poller() or str()
        :param template: HostTemplate(), list() of HostTemplate() or str()
        :param hg: HostGroup(), list() of HostGroup() or str()
        :return:
        """
        if template and isinstance(template, HostTemplate):
            _hosttmpl = template.name
        elif template and isinstance(template, list):
            tmp_hosttmpl = list()
            for htmpl in template:
                tmp_hosttmpl.append(htmpl.name)
            _hosttmpl = "|".join(tmp_hosttmpl)
        elif template and isinstance(template, str):
            _hosttmpl = template
        else:
            raise ValueError("HostTemplate must be defined")

        if hg and isinstance(hg, HostGroup):
            _hg = hg.name
        elif hg and isinstance(hg, list):
            tmp_hg = list()
            for group in hg:
                tmp_hg.append(group.name)
            _hg = "|".join(tmp_hg)
        elif hg and isinstance(hg, str):
            _hg = hg
        else:
            raise ValueError("HostGroups must be defined")

        if instance and isinstance(instance, Poller):
            _instance = instance.name
        elif instance and isinstance(instance, str):
            _instance = instance
        else:
            raise ValueError("Instance (poller) must be defined")

        values = [
            name,
            alias,
            ip,
            str(_hosttmpl),
            str(_instance),
            str(_hg)
        ]
        return self.webservice.call_clapi('add', 'HOST', values)

    @CentreonDecorator.post_refresh
    def delete(self, host):
        return self.webservice.call_clapi('del', 'HOST', host.name)

    @CentreonDecorator.post_refresh
    def setparam(self, host, name, value):
        values = [host.name, name, value]
        return self.webservice.call_clapi('setparam', 'HOST', values)

    #def getservices(self, host):
    #    values = {'searchHost': host.name}
    #    return self.webservice.centreon_realtime('list', 'services', values)


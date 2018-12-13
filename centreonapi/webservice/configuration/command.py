# -*- coding: utf-8 -*-

from centreonapi.webservice.configuration.common import *
from bs4 import BeautifulSoup
from overrides import overrides


class Command(CentreonObject):

    def __init__(self, properties):
        self.webservice = Webservice.getInstance()
        self.id = properties.get('id')
        self.name = properties.get('name')
        self.line = self._build_command_line(properties.get('line'))
        self.type = properties.get('type')

    @staticmethod
    def _build_command_line(line):
        if line:
            if isinstance(line, list):
                command_line = "|".join(line)
            else:
                command_line = line
            command_line_soup = BeautifulSoup(command_line, "html.parser")
            command_line_soup = str(command_line_soup).replace('<br/>', '\n')
            command_line_soup = str(command_line_soup).replace('&amp;', '&')
            return str(command_line_soup)
        else:
            return ""

    def setparam(self, name, value):
        values = [
            self.name,
            name,
            value
        ]
        return self.webservice.call_clapi('setparam', 'CMD', values)


class Commands(CentreonDecorator, CentreonClass):
    """
    Centreon Web Command object
    """
    def __init__(self):
        super(Commands, self).__init__()
        self.commands = dict()

    def __contains__(self, name):
        return name in self.commands.keys()

    def __getitem__(self, name):
        if not self.commands:
            self.list()
        if name in self.commands.keys():
            return self.commands[name]
        else:
            raise ValueError("Command %s not found" % name)

    def _refresh_list(self):
        self.commands.clear()
        for command in self.webservice.call_clapi('show', 'CMD')['result']:
            command_obj = Command(command)
            self.commands[command_obj.name] = command_obj

    @CentreonDecorator.pre_refresh
    def list(self):
        return self.commands

    @CentreonDecorator.post_refresh
    def add(self, cmdname, cmdtype, cmdline, post_refresh=True):
        values = [
            cmdname,
            cmdtype,
            cmdline
        ]
        return self.webservice.call_clapi('add', 'CMD', values)

    @CentreonDecorator.post_refresh
    def delete(self, command, post_refresh=True):
        value = str(self._build_param(command, Command)[0])
        return self.webservice.call_clapi('del', 'CMD', value)




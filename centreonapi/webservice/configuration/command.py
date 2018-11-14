# -*- coding: utf-8 -*-

from centreonapi.webservice import Webservice
from bs4 import BeautifulSoup


class CommandObj(object):

    def __init__(self, properties):
        self.id = properties['id']
        self.name = properties['name']
        self.line = self._build_command_line(properties['line'])
        self.type = properties['type']

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()


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


class Command(object):
    """
    Centreon Web Command object
    """

    def __init__(self):
        """
        Constructor
        """
        self.webservice = Webservice.getInstance()
        self.commands = dict()

    def get(self, name):
        if not self.commands:
            self.list()
        return self.commands[name]

    def exist(self, name):
        if not self.commands:
            self.list()
        if name in self.commands:
            return True
        else:
            return False

    def list(self):
        """
        List resource
        """
        for command in self.webservice.call_clapi('show', 'CMD')['result']:
            command_obj = CommandObj(command)
            self.commands[command_obj.name] = command_obj
        return self.commands

    def add(self, cmdname, cmdtype, cmdline):
        """
        add new command
        """
        values = [
            cmdname,
            cmdtype,
            cmdline
        ]
        return self.webservice.call_clapi('add', 'CMD', values)

    def delete(self, cmdname):
        """
        Delete a command
        """
        return self.webservice.call_clapi('del', 'CMD', cmdname)

    def setparam(self, cmdname, name, value):
        """
        SetParam on command
        """
        values = [
            cmdname,
            name,
            value
        ]
        return self.webservice.call_clapi('setparam', 'CMD', values)


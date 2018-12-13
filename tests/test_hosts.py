from centreonapi.centreon import Centreon
from centreonapi.centreon import Webservice
from mock import patch
import pytest
import responses
import json
import os
from path import Path


if os.path.isdir('tests'):
    config_dir = Path('tests')
    resource_dir = Path('tests/resources')
else:
    config_dir = Path('.')
    resource_dir = Path('./resources')


class TestConnect:
    @responses.activate
    def test_connection(self):
        url = "http://api.domain.tld/centreon"
        username = "mytest"
        password = "mypass"
        mytoken = "NTc1MDU3MGE3M2JiODIuMjA4OTA2OTc="
        wsresponses = '{"authToken": "NTc1MDU3MGE3M2JiODIuMjA4OTA2OTc="}'
        responses.add(responses.POST,
                      'http://api.domain.tld/centreon/api/index.php?action=authenticate',
                      body=wsresponses, status="200", content_type='application/json')

        myconn = Webservice.getInstance(url, username, password)
        myconn.auth()
        print myconn.auth_token
        assert mytoken == myconn.auth_token


class TestHosts:
    @pytest.fixture()
    @responses.activate
    def centreon_con(self):
        url = "http://api.domain.tld/centreon"
        username = "mytest"
        password = "mypass"

        wsresponses = '{"authToken": "NTc1MDU3MGE3M2JiODIuMjA4OTA2OTc="}'
        responses.add(responses.POST,
                  'http://api.domain.tld/centreon/api/index.php?action=authenticate',
                  body=wsresponses, status="200", content_type='application/json')
        return Centreon(url, username, password)

    @responses.activate
    def test_host_list(self, centreon_con):
        with open(resource_dir / 'test_hosts_list.json') as data:
            wsresponses = json.load(data)
        responses.add(responses.POST,
                  'http://api.domain.tld/centreon/api/index.php?action=action&object=centreon_clapi',
                  json=wsresponses, status="200", content_type='application/json')
        res = centreon_con.hosts.get('mail-uranus-frontend')
        assert res.id == "12"

    @responses.activate
    def test_host_not_exist(self, centreon_con):
        with open(resource_dir / 'test_hosts_list.json') as data:
            wsresponses = json.load(data)
        responses.add(responses.POST,
                      'http://api.domain.tld/centreon/api/index.php?action=action&object=centreon_clapi',
                      json=wsresponses, status="200", content_type='application/json')
        with pytest.raises(ValueError):
            centreon_con.hosts.get('empty')



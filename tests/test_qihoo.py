import pytest  # noqa
from unittest.mock import Mock, patch

from qihoo.qh import Qihoo, Router, BlackList, SpeedLimit, Devices, VirtualService


@pytest.fixture
def mock_client():
    with patch('httpx.Client') as mock:
        client = Mock()
        mock.return_value = client
        yield client


@pytest.fixture
def router(mock_client):
    router = Router()
    router.baseurl = 'http://router.test'
    router.req = mock_client
    return router


@pytest.fixture
def qihoo(mock_client):
    with patch('qihoo.qh.Qihoo._login'):
        router = Qihoo('test_user', 'test_pass')
        return router


class TestBlackList:
    def test_list(self, router):
        plugin = BlackList(router)
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {'mac': '00:11:22:33:44:55'},
                {'mac': 'AA:BB:CC:DD:EE:FF'}
            ]
        }
        router.req.get.return_value = mock_response

        result = plugin.list()

        router.req.get.assert_called_once_with(
            'http://router.test/app/devices/webs/getblacklist.cgi'
        )
        assert result == mock_response.json()

    def test_exists(self, router):
        plugin = BlackList(router)
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {'mac': '00:11:22:33:44:55'},
                {'mac': 'AA:BB:CC:DD:EE:FF'}
            ]
        }
        router.req.get.return_value = mock_response

        assert plugin.exists('00:11:22:33:44:55') is True
        assert plugin.exists('11:11:11:11:11:11') is False

    def test_add(self, router):
        plugin = BlackList(router)
        mock_response = Mock()
        mock_response.json.return_value = {'code': 0}
        router.req.post.return_value = mock_response

        result = plugin.add('00:11:22:33:44:55')

        router.req.post.assert_called_once_with(
            'http://router.test/app/devices/webs/setblacklist.cgi',
            data={'mac': '00:11:22:33:44:55'}
        )
        assert result == {'code': 0}


class TestSpeedLimit:
    def test_set(self, router):
        plugin = SpeedLimit(router)
        mock_response = Mock()
        mock_response.json.return_value = {'code': 0}
        router.req.post.return_value = mock_response

        result = plugin.set('00:11:22:33:44:55', 1000, 2000)

        router.req.post.assert_called_once_with(
            'http://router.test/app/devices/webs/setspeedlimit.cgi',
            data={
                'enable': '1',
                'mac': '00:11:22:33:44:55',
                'upload': '1000',
                'download': '2000'
            }
        )
        assert result == {'code': 0}


class TestDevices:
    def test_list(self, router):
        plugin = Devices(router)
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {'name': 'device1', 'mac': '00:11:22:33:44:55'},
                {'name': 'device2', 'mac': 'AA:BB:CC:DD:EE:FF'}
            ]
        }
        router.req.get.return_value = mock_response

        result = plugin.list()

        router.req.get.assert_called_once_with(
            'http://router.test/app/devices/webs/getdeviceslist.cgi'
        )
        assert result == mock_response.json()['data']


class TestVirtualService:
    def test_add(self, router):
        plugin = VirtualService(router)
        mock_response = Mock()
        mock_response.json.return_value = {'code': 0}
        router.req.post.return_value = mock_response

        result = plugin.add(
            name='test_service',
            internal_ip='192.168.1.100',
            external_port='8080',
            internal_port='80'
        )

        router.req.post.assert_called_once_with(
            'http://router.test/app/portmap/webs/virtual_service_add_del.cgi',
            data={
                'name': 'test_service',
                'in_ip': '192.168.1.100',
                'protocol': 'tcp',
                'out_start_port': '8080',
                'out_end_port': '8080',
                'in_start_port': '80',
                'in_end_port': '80',
                'uiname': 'ALL',
                'mode': 0
            }
        )
        assert result == {'code': 0}

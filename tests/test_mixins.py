"""测试 Mixin """
import json

import pytest

import config


class TestLoginMixin:
    """测试 Qihoo360LoginMixin"""

    def test_get_rank_key(self, router):
        result = router.get_rank_key()
        print(result)
        assert 'rand_key' in result
        assert 'key_index' in result

    def test_login(self, router):
        cookies = router.login(username=router.user.username,
                               password=router.user.password)
        print(cookies)
        assert 'Qihoo_360_login' in cookies
        assert 'Token-ID' in cookies


class TestBlacklistMixin:
    """测试 Qihoo360BlacklistMixin"""

    @pytest.fixture(scope='class')
    def device(self):
        """环境变量中的黑名单mac地址"""
        assert len(config.BLACKLISTS) > 0
        device = config.BLACKLISTS[0]
        yield device

    @pytest.mark.asyncio
    async def test_get_blacklist(self, router):
        result = await router.get_blacklist()
        print(json.dumps(result, ensure_ascii=False))
        assert 'err_no' in result and result['err_no'] == '0'

    @pytest.mark.asyncio
    async def test_set_blacklist(self, router, device):
        mac = device.mac
        result = await router.set_blacklist(mac=mac)
        # print(json.dumps(result))
        assert 'err_no' in result and result['err_no'] == '0'
        is_in_blacklist = await router.is_in_blacklist(mac)
        assert is_in_blacklist is True

    @pytest.mark.asyncio
    async def test_cancel_blacklist(self, router, device):
        mac = device.mac
        result = await router.cancel_blacklist(mac=mac)
        # print(json.dumps(result))
        assert 'err_no' in result and result['err_no'] == '0'
        is_in_blacklist = await router.is_in_blacklist(mac)
        assert is_in_blacklist is False


class TestSpeedlimitMixin:
    """测试 Qihoo360SpeedlimitMixin"""

    @pytest.fixture(scope='class')
    def device(self):
        """环境变量中的黑名单mac地址"""
        assert len(config.SPEEDLIMIT_LIST) > 0
        device = config.SPEEDLIMIT_LIST[0]
        yield device

    @pytest.mark.asyncio
    async def test_set_speed_limit(self, router, device):
        result = await router.set_speed_limit(mac=device.mac,
                                              upload=device.limit_speed,
                                              download=device.limit_speed)
        print(result)
        assert 'err_no' in result and result['err_no'] == '0'

    @pytest.mark.asyncio
    async def test_cancel_speed_limit(self, router, device):
        result = await router.cancel_speed_limit(mac=device.mac, )
        print(result)
        assert 'err_no' in result and result['err_no'] == '0'


class TestDevicesMixin:
    """测试 Qihoo360DevicesMixin"""

    @pytest.mark.asyncio
    async def test_mesh_get_topology_info(self, router):
        data = await router.mesh_get_topology_info()
        print(json.dumps(data))

    @pytest.mark.asyncio
    async def test_get_device_list(self, router):
        devices = await router.device_list()
        for d in devices:
            print(d)


class TestVirtualServiceMixin:
    """测试 VirtualServiceMixin"""

    def test_virtual_service_list(self, router):
        vs_list = router.virtual_service_list()
        print(vs_list)

    def test_virtual_service_add(self, router):
        result = router.virtual_service_add(name="pytest1",
                                            internal_ip="192.168.x.x",
                                            external_port=18888,
                                            internal_port=16666)
        assert result == ['SUCCESS']

    def test_virtual_service_del(self, router):
        result = router.virtual_service_del(name="pytest1",
                                            internal_ip="192.168.x.x",
                                            external_port=18888,
                                            internal_port=16666)
        assert result == ['SUCCESS']

    def test_virtual_service_clean(self, router):
        result = router.virtual_service_clean()
        assert result == ['SUCCESS']

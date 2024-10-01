"""
测试 utils模块
"""
import pytest
from utils import is_in_hour_minute_period


@pytest.mark.parametrize("time_period,time_,result",
                         [('12:00-13:00', None, False),
                          ('08:30-09:30', '09:00', True)])
def test_is_in_hour_minute_period_single(time_period, time_, result):
    """测试单个时间段"""
    assert is_in_hour_minute_period(time_period, time_=time_) is result


@pytest.mark.parametrize("time_period,time_,result",
                         [(['12:00-13:00', '18:00-18:59'], None, False),
                          (['08:30-09:30', '10:00-11:00'], '09:00', True)])
def test_is_in_hour_minute_period_multi(time_period, time_, result):
    """测试多个时间段"""
    assert is_in_hour_minute_period(*time_period, time_=time_) is result

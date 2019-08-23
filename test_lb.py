from loadbalancer import LoadBalancer
import pytest


class Test:
    def test_balance(self):
        lb = LoadBalancer(umax=2, ttask=4)
        lb.process([1, 3, 0, 1, 0, 1])
        assert lb.snapshots == ['1', '2,2', '2,2', '2,2,1', '1,2,1', '2', '2', '1', '1', '0']

    def test_coast_calculator(self):
        lb = LoadBalancer(umax=2, ttask=4)
        lb.process([1, 3, 0, 1, 0, 1])
        assert lb.total_coast == 15

    def test_invalid_umax_size(self):
        with pytest.raises(Exception):
            assert LoadBalancer(umax=11, ttask=4)

    def test_invalid_ttask_max(self):
        with pytest.raises(Exception):
            assert LoadBalancer(umax=1, ttask=40)

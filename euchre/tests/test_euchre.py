
# TESTS
import pytest
from .euchre.utils import *


def test_return_off_suit():
    assert get_teammate('p2') == 'p4'
    assert get_teammate('p4') == 'p2'
    assert get_teammate('p1') == 'p3'


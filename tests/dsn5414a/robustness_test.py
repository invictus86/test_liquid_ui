"""
    DSN5414a General loader test
    Author: ivan.zhao@ekt-digital.com
    data: 2020-7-14
"""
import os
import sys
import time
import stbt
import utils
from dsn5414a import v5utils

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from ektlib import ekt_dta, ekt_mod, ekt_diseqc, ekt_status, ekt_button, ekt_rds


def test_100_times_channel_switch():
    """
    100 times of channel switch with the fastest speed
    :return: None
    """
    pass

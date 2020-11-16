#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from liquid_ui import v5utils

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from ektlib import ekt_dta, ekt_mod, ekt_diseqc, ekt_status, ekt_button, ekt_rds


def test_100_times_channel_switch():
    """
    1、播放码流(测试开始前先执行smoke test的case，进行锁台操作)
    2、连续切台100次
    3、检测测试是否成功
    100 times of channel switch with the fastest speed
    :return: None
    """
    for _ in range(100):
        stbt.press("KEY_DOWN")
    time.sleep(3)
    stbt.wait_for_motion(timeout_secs=3)

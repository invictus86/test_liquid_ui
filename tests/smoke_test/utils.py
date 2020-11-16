"""
    DSN7414v General loader test
    Author: ivan.zhao@ekt-digital.com
    data: 2019-10-17

"""
import os
import sys
import socket
from socket import *
import json

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)


import time
import stbt


def input_digital(keys_list):
    """
    :param number:
    :return:
    """
    keys = {'0': 'KEY_0',
            '1': 'KEY_1',
            '2': 'KEY_2',
            '3': 'KEY_3',
            '4': 'KEY_4',
            '5': 'KEY_5',
            '6': 'KEY_6',
            '7': 'KEY_7',
            '8': 'KEY_8',
            '9': 'KEY_9',
            'A': 'KEY_PLAY',
            'B': 'KEY_STOP',
            'C': 'KEY_FAST_BACKWORD',
            'D': 'KEY_FAST_FORWARD',
            'E': 'KEY_PREVIOUS',
            'F': 'KEY_NEXT',
            }

    for key in keys_list:
        stbt.press(key)
        time.sleep(0.5)
    time.sleep(1)

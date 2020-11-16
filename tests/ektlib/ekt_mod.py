"""

version v0.1
author: kim.tang@ekt-digital.com
history:
v0.1:
init release
"""

import stbt
import time


class EktTestFail(stbt.UITestFailure):
    pass

def mult_press(key, count):
    """
    :param key:
    :param count:
    :return:
    """
    for i in range(0, count):
        stbt.press(key)
        time.sleep(1)
    time.sleep(1)


def input_digital(number):
    """
    :param number:
    :return:
    """
    keys = {    '0': 'KEY_0',
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
    for i in range(0,len(number)):
        stbt.press(keys[number[i]])
        time.sleep(0.5)
        # print keys[number[i]]
    time.sleep(1)

if __name__ == '__main__':
    mult_press("KEY_OK", 3)
    input_digital('7DE')

"""
This module controls the external IR transmitter with large power,
so it can control multiple STBs at the same time
author: loren.huang@ekt-digital.com
date: 2018-10-8
"""
from RedRatHub import redrathub


class EktKeyPress(object):
    @staticmethod
    def key_press(key, index=4,ruc="default"):
        """
        Controls the external RedRat-X IR device to send an IR signal.
        :param key: the name of the IR signal to be sent out.
        :param index: the IR transmitter output port index.
        :param ruc: the RCU key data file name.
        :return: None.
        """
        if ruc == "default":
            redrathub.press(key=key, output=index)
        else:
            redrathub.press(key=key, output=index,dataset=ruc)

    # @staticmethod
    # def key_press_ext(index, key):
    #     redrathub.press(key=key, output=index)

    @staticmethod
    def key_press_get_ports():
        """
        Get the total ports of the external IR device.
        :return:  the total ports of the IR device(4 for the current RedRat-X device).
        """
        return 4

    @staticmethod
    def close():
        redrathub.CloseSocket()


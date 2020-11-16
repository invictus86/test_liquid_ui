"""
This module controls the HDMI switch device,
it can select one of the five boxes HDMI output
to connect to the STB-Tester's HDMI input.
author: loren.huang@ekt-digital.com
date: 2018-10-8
"""
import time

import stbt


class EktHdmiSwitch(object):
    current_port = 1

    @classmethod
    def hdmi_switch_to(cls, index):
        """
        Select one HDMI port indicated by "index".
        :param index: the port index of the HDMI switch (1 ~ 5).
        :return: None.
        """
        stbt.press(index)
        cls.current_port = int(index[-1])
        print "switch to:%s" % index

    @staticmethod
    def hdmi_get_current_ports():
        """
        Get the ports that currently connect to the HDMI switch.
        :return: the list of ports that connected a set_top box.
        """
        connect_port = []
        time.sleep(60)
        for i in range(1, 6):

            stbt.press("KEY_HDMI_%d" % i)
            time.sleep(5)
            try:
                stbt.wait_for_motion(timeout_secs=5)
                connect_port.append("HDMI_%d" % i)
            except :
                pass
        print "detect HDMI list:", connect_port
        return connect_port

    @classmethod
    def hdmi_switch_prev(cls):
        """
        Switch to the previous HDMI port.
        :return: None.
        """
        stbt.press("KEY_HDMI_PREV")
        if cls.current_port != 1:
            cls.current_port -= 1
        print "switch to prev"

    @classmethod
    def hdmi_switch_next(cls):
        """
        Switch to the next HDMI port.
        :return: None.
        """
        stbt.press("KEY_HDMI_NEXT")
        if cls.current_port != 5:
            cls.current_port += 1
        print "switch to next"

    @staticmethod
    def hdmi_get_ports():
        """
        Get the total ports of the HDMI switch.
        :return: the total ports of the HDMI switch (5 for the current HDMI switch).
        """
        return 5
    
    @classmethod
    def hdmi_get_current_port(cls):
        """
        Get the current port index of the HDMI switch.
        :return: the current port index of the HDMI switch.
        """
        return cls.current_port

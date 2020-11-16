import os
import sys
import socket
import string
import time
import string
import ekt_net


class EktRds(object):
    """

    """

    def __init__(self, net):
        self.net = net
        self.usb_switch_none()
        # self.usb_switch_stb()
        time.sleep(2)

    def power_on(self):
        """

        :return:
        """
        cmd = 'RDS:POWER_ON'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def power_off(self):
        """

        :return:
        """
        cmd = 'RDS:POWER_OFF'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def usb_switch_pc(self):
        """

        :return:
        """
        cmd = 'RDS:USB_PC'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def usb_switch_stb(self):
        """

        :return:
        """
        cmd = 'RDS:USB_STB'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def usb_switch_none(self):
        """

        :return:
        """
        cmd = 'RDS:USB_NONE'
        paras = ''
        return self.net.send_ok(cmd, paras)


def _test_RDS_ctl():
    print "RDS control test start"
    host = '127.0.0.1'
    port = 8900
    net = ekt_net.EktNetClient(host, port)
    rds = EktRds(net)

    rds.power_off()
    time.sleep(5)
    rds.power_on()
    time.sleep(5)
    rds.usb_switch_pc()
    time.sleep(20)
    rds.usb_switch_none()

    del rds
    del net
    print "RDS control test end"


def _test_close_usb():
    print "RDS control test start"
    host = '127.0.0.1'
    port = 8900
    net = ekt_net.EktNetClient(host, port)
    rds = EktRds(net)

    time.sleep(3)
    rds.power_off()

    print "RDS control test end"


if __name__ == '__main__':
    _test_close_usb()

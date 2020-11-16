"""
    control ethernet Connect and disconnect
    Author: ivan.zhao@ekt-digital.com
    data: 2020-7-24
"""

import time
import ekt_net


class EktEthernet(object):
    """
    control cable Connect and disconnect
    """

    def __init__(self, net):
        self.net = net

    def ethernet_connect(self):
        """
        control ethernet connect
        :return:
        """
        cmd = 'RDSP:RJ45_ON'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def ethernet_disconnect(self):
        """
        control ethernet disconnect
        :return:
        """
        cmd = 'RDSP:RJ45_OFF'
        paras = ''
        return self.net.send_ok(cmd, paras)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8900
    net = ekt_net.EktNetClient(host, port)

    cab = EktEthernet(net)
    cab.ethernet_connect()
    # time.sleep(2)
    # cab.ethernet_disconnect()

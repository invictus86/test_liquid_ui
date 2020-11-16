"""
    control front button
    Author: ivan.zhao@ekt-digital.com
    data: 2020-7-24
"""

import time
import ekt_net
import ekt_rds
import ekt_status


class EktButton(object):
    """
    control front button
    """

    def __init__(self, net):
        self.net = net

    def click_key1(self):
        """
        Press key1 and release immediately
        :return:
        """
        cmd = 'RDSP:PRESS_KEY1'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def click_key2(self):
        """
        Press key2 and release immediately
        :return:
        """
        cmd = 'RDSP:PRESS_KEY2'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def click_key3(self):
        """
        Press key3 and release immediately
        :return:
        """
        cmd = 'RDSP:PRESS_KEY3'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def click_key4(self):
        """
        Press key4 and release immediately
        :return:
        """
        cmd = 'RDSP:PRESS_KEY4'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def click_key5(self):
        """
        Press key5 and release immediately
        :return:
        """
        cmd = 'RDSP:PRESS_KEY5'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def key1_up(self):
        """
        Release the key1
        :return:
        """
        cmd = 'RDSP:KEY1_UP'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def key2_up(self):
        """
        Release the key2
        :return:
        """
        cmd = 'RDSP:KEY2_UP'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def key3_up(self):
        """
        Release the key3
        :return:
        """
        cmd = 'RDSP:KEY3_UP'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def key4_up(self):
        """
        Release the key4
        :return:
        """
        cmd = 'RDSP:KEY4_UP'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def key5_up(self):
        """
        Release the key5
        :return:
        """
        try:
            cmd = ':RDSP:KEY5_UP\r\n'
            self.net.send_data(cmd)
        except:
            time.sleep(3)
            cmd = ':RDSP:KEY5_UP\r\n'
            self.net.send_data(cmd)

    def key1_down(self):
        """
        Long press the key1
        :return:
        """
        cmd = 'RDSP:KEY1_DOWN'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def key2_down(self):
        """
        Long press the key2
        :return:
        """
        cmd = 'RDSP:KEY2_DOWN'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def key3_down(self):
        """
        Long press the key3
        :return:
        """
        cmd = 'RDSP:KEY3_DOWN'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def key4_down(self):
        """
        Long press the key4
        :return:
        """
        cmd = 'RDSP:KEY4_DOWN'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def key5_down(self):
        """
        Long press the key5
        :return:
        """
        try:
            cmd = ':RDSP:KEY5_DOWN\r\n'
            self.net.send_data(cmd)
        except:
            time.sleep(3)
            cmd = ':RDSP:KEY5_DOWN\r\n'
            self.net.send_data(cmd)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8900
    net = ekt_net.EktNetClient(host, port)

    btn = EktButton(net)
    rds = ekt_rds.EktRds(net)
    # btn.click_key1()
    # time.sleep(2)
    # btn.click_key2()
    # time.sleep(2)
    # btn.click_key3()
    # time.sleep(2)
    # btn.click_key4()
    # time.sleep(2)
    # btn.click_key5()

    rds.power_off()
    time.sleep(3)
    btn.key5_down()
    # time.sleep(5)
    rds.power_on()
    time.sleep(6)
    btn.key5_up()

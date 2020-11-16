import time
import ekt_net
import json


class EktXshell(object):
    """

    """

    def __init__(self, net):
        self.net = net

    def set_usb_upgrade(self):
        """
        set usb upgrade
        :return:
        """
        data = {"set_data": 1}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)

    def set_usb_engineer_upgrade(self):
        """
        set usb engineer upgrade
        :return:
        """
        data = {"set_data": 2}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)

    def set_ota_upgrade(self):
        """
        set ota upgrade
        :return:
        """
        data = {"set_data": 3}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)

    def set_ota_force_upgrade(self):
        """
        set ota force upgrade
        :return:
        """
        data = {"set_data": 4}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)

    def set_change_pid_area_ota_upgrade(self):
        """
        set change pid area ota upgrade
        :return:
        """
        data = {"set_data": 5}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)

    def set_turning_frequency_960_ota_upgrade(self):
        """
        set change pid area ota upgrade
        :return:
        """
        data = {"set_data": 6}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)

    def set_turning_frequency_1500_ota_upgrade(self):
        """
        set change pid area ota upgrade
        :return:
        """
        data = {"set_data": 7}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)

    def set_turning_frequency_1800_ota_upgrade(self):
        """
        set change pid area ota upgrade
        :return:
        """
        data = {"set_data": 8}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)

    def set_turning_frequency_2150_ota_upgrade(self):
        """
        set change pid area ota upgrade
        :return:
        """
        data = {"set_data": 9}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)

    def set_symbol_rate_5_ota_upgrade(self):
        """
        set symbol rate 5M ota upgrade
        :return:
        """
        data = {"set_data": 10}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)

    def set_symbol_rate_10_ota_upgrade(self):
        """
        set symbol rate 10M ota upgrade
        :return:
        """
        data = {"set_data": 11}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)

    def set_symbol_rate_30_ota_upgrade(self):
        """
        set symbol rate 30M ota upgrade
        :return:
        """
        data = {"set_data": 12}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)

    def set_symbol_rate_45_ota_upgrade(self):
        """
        set symbol rate 45M ota upgrade
        :return:
        """
        data = {"set_data": 13}
        cmd = json.dumps(data)
        return self.net.send_rec(cmd)


if __name__ == '__main__':
    host = '192.168.1.24'
    port = 9991
    net = ekt_net.EktNetClient(host, port)
    xsh = EktXshell(net)

    # xsh.set_usb_upgrade()
    # time.sleep(2)
    # xsh.set_usb_engineer_upgrade()
    # time.sleep(2)
    # xsh.set_ota_upgrade()
    # time.sleep(2)
    # xsh.set_ota_force_upgrade()

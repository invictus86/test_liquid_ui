"""

version v0.1
author: kim.tang@ekt-digital.com
history:
v0.1:
init release
"""

import time
import ekt_net


class EktRelay(object):
    def __init__(self, ip="192.168.0.105", port=5000):
        self.ip = ip
        self.port = port
        self.sock = ekt_net.EktNetClient(self.ip, self.port)
        self.sock.rec_data()
        # print "EktRelay start"

    def __del__(self):
        del self.sock
        # print "EktRelay stop"

    def relay_on(self, id):
        """
        open a relay.
        :param id: int
            1, the first relay.
            2, the second relay.
        :return:
        """
        paras = 'on%d' % (id)
        self.sock.send_rec(paras)

    def relay_off(self, id):
        """
        close a relay.
        :param id: see 'relay_on'
        :return:
        """
        paras = 'off%d' % (id)
        self.sock.send_rec(paras)

    def relay_state(self, id):
        """
        read a relay status.
        :param id: see 'relay_on'
        :return: None.
        """
        paras = 'read%d' % (id)
        print self.sock.send_rec(paras)

    def is_relay_on(self,id):
        """
        detect the status of relay
        :param id:
        :return: True ,if the status is on.
        """
        status = self.sock.send_rec("read%d"%id)
        if status=="on%d"%id:
            return True
        else:
            return False


def _test_relay1_poweron():
    en = EktRelay()
    en.relay_on(1)
    
    
def _test_relay1_poweroff():
    en = EktRelay()
    en.relay_off(1)


def example_relay2():
    en = EktRelay()
    en.relay_off(2)
    time.sleep(3)
    en.relay_on(2)
    time.sleep(3)
    en.relay_off(2)

if __name__ == '__main__':
    _test_relay1_poweron()
    # test_relay2()

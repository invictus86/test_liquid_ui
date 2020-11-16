import os
import sys
import socket
import string
import time
import string
import ekt_net
import ekt_rds


class EktFileCfg(object):
    """

    """
    def __init__(self, net):
        self.net = net
        self.config = {}
        self.get_config()
        self.clean_file = self.config.get('CLEANFILE', None)
        self.load_file = self.config.get('LOADFILE', None)

    def get_config(self):
        """
        ('OTASYMBOLRATE', '6875')
        ('CD5PATH', 'D:\\autotest\\CD5\\')
        ('TSPATH', 'D:\\Temporary\\V5Stream\\')
        ('USBPATH', 'G:\\')
        ('OTATYPE', '6')
        ('OTAANNEX', '2')
        ('OTACODERATE', '1')
        ('LOADFILE', 'Irdeto_0238_0029.CD5')
        ('OTAFREQ', '330000')
        ('OTABANDWIDTH', '4')
        ('CLEANFILE', 'EKCleanSPCBKey.CD5')
        ('PID', '7D3')

        :return:
        """
        cmd = 'DOC:CONFIG'
        paras = ''
        ret, data = self.net.send_ok(cmd, paras)
        for str_data in data.split('#')[1:]:
            key_cfg, value_cfg = str_data.split('=')
            self.config[key_cfg] = value_cfg
        return ret

    def usb_file(self, filename):
        return self.config.get('USBPATH', '') + filename

    def cd5_file(self, filename):
        return self.config.get('CD5PATH', '') + filename

    def ts_file(self, filename):
        return self.config.get('TSPATH', '') + filename

    def copy_file(self, src, dst):
        """

        :return:
        """
        cmd = 'DOC:COPY'
        paras = '%s %s' % (src, dst)
        return self.net.send_ok(cmd, paras)

    def move_file(self, src, dst):
        """

        :return:
        """
        cmd = 'DOC:MOVE'
        paras = '%s %s' % (src, dst)
        return self.net.send_ok(cmd, paras)

    def del_file(self, file):
        """

        :return:
        """
        cmd = 'DOC:DEL'
        paras = '%s' % file
        return self.net.send_ok(cmd, paras)

    def app_exec(self, para):
        """

        :return:
        """
        cmd = 'APP:EXEC'
        paras = '%s' % para
        return self.net.send_ok(cmd, paras)

    def app_close(self):
        """

        :return:
        """
        cmd = 'APP:CLOSE'
        paras = ''
        return self.net.send_ok(cmd, paras)


def _test_file_ctl():
    print "file test start"
    host = '127.0.0.1'
    port = 8900
    src_file = r'D:\autotest\IrdetoKeyDownload\EGKX1DDEVV5.KEE'
    dst_file = r'D:\autotest\Irdeto_0238_0029.CD5'
    net = ekt_net.EktNetClient(host, port)
    doc = EktFileCfg(net)

    doc.copy_file(src_file, dst_file)

    del doc
    del net
    print "file test end"


def _test_file_and_usb_ctl():
    print "file test start"
    host = '127.0.0.1'
    port = 8900
    src_file = r'D:\autotest\IrdetoKeyDownload\EGKX1DMANV5.KEE'
    dst_file = r'F:\Irdeto_0238_0029.CD5'
    net = ekt_net.EktNetClient(host, port)
    doc = EktFileCfg(net)
    rds = ekt_rds.EktRds(net)

    rds.usb_switch_none()
    time.sleep(5)
    rds.usb_switch_pc()
    time.sleep(8)
    doc.copy_file(src_file, dst_file)
    time.sleep(5)
    rds.usb_switch_none()

    del doc
    del rds
    del net
    print "file test end"


def _test_cmd_execute():
    print "file test start"
    host = '127.0.0.1'
    port = 8900
    str_para = r'D:\autotest\CD5\BAD_SUBVAR.CD5'
    net = ekt_net.EktNetClient(host, port)
    doc = EktFileCfg(net)
    rds = ekt_rds.EktRds(net)

    # rds.power_off()
    # time.sleep(4)
    doc.app_exec(str_para)
    # rds.power_on()
    # time.sleep(30)
    doc.app_close()

    del doc
    del net
    print "file test end"

if __name__ == '__main__':
    _test_cmd_execute()

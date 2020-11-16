"""

version v0.1
author: kim.tang@ekt-digital.com
history:
v0.1:
init release, for SpRcApi
"""

import os
import sys
import socket
import string
import time
import string
import ekt_net


class EktDtDevice(object):
    # ----------------------define-----------------------
    # DVB modulation
    MOD_DTMB = 3
    MOD_DVBS = 5
    MOD_DVBS2 = 6
    MOD_DVBT = 7
    MOD_DVBT2 = 8
    MOD_ISDBT = 12
    MOD_J83A = 13  # J.83 annex A (DVB-C)
    MOD_J83B = 14  # J.83 annex B ("American QAM")

    # DVB type
    DTA_DVBS_QPSK = '0'
    DTA_DVBS2_QPSK = '32'
    DTA_DVBS2_8PSK = '33'
    DTA_DVBT = '9'
    DTA_DVBT2 = '11'
    DTA_DTMB = '48'
    DTA_ISDBT = '12'
    DTA_QAM4 = '3'
    DTA_QAM16 = '4'
    DTA_QAM32 = '5'
    DTA_QAM64 = '6'
    DTA_QAM128 = '7'
    DTA_QAM256 = '8'

    # DVBC-annex
    DTA_J83_A = '2'  # DVB-C
    DTA_J83_B = '3'  # QAM-B
    DTA_J83_C = '1'

    # DVBT
    DTA_6MHZ = '2'
    DTA_7MHZ = '3'
    DTA_8MHZ = '4'

    # DVBS2
    DTA_1_2 = '0'
    DTA_2_3 = '1'
    DTA_3_4 = '2'
    DTA_4_5 = '3'
    DTA_5_6 = '4'
    DTA_6_7 = '5'
    DTA_7_8 = '6'
    DTA_1_4 = '7'
    DTA_1_3 = '8'
    DTA_2_5 = '9'
    DTA_3_5 = '10'
    DTA_8_9 = '11'
    DTA_9_10 = '12'

    # BOOL
    DTA_FALSE = 0
    DTA_TRUE = 1

    # -------------------------------------------------

    def __init__(self, net):
        """
        init
        """
        self.type = ''
        self.mod = ''
        self.net = net
        print "EktDtDevice start"

    def __del__(self):
        """
        delete net client
        """
        pass

        print "EktDtDevice exit"

    def set_device(self, type, mod):
        """
        :param type: the type of dectek card, like 115, 107
        :param mod:
            MOD_DTMB
            MOD_DVBS
            MOD_DVBS2
            MOD_DVBT
            MOD_DVBT2
            MOD_ISDBT
            MOD_J83A  # J.83 annex A (DVB-C)
            MOD_J83B  # J.83 annex B ("American QAM")
        :return:
        """
        self.type = type
        self.mod = mod
        cmd = 'DTA:TYPE'
        paras = '%d %d' % (type, mod)
        return self.net.send_ok(cmd, paras)

    def set_freq(self, freq):
        """
        :param freq: modulation carrier frequency in KHz
        :return:
        """
        cmd = 'DTA:FREQ'
        paras = '%d' % (freq)
        return self.net.send_ok(cmd, paras)

    def set_tsrate(self, rate):
        """
        :param rate: modulation carrier ts rate in bps
        :return:
        """
        cmd = 'DTA:TSRATE'
        paras = '%d' % (rate)
        return self.net.send_ok(cmd, paras)

    def set_sym_rate(self, rate):
        """
        :param rate: symbol rate in Kbd. like 6875 or 27500
        :return:
        """
        cmd = 'DTA:SYMRATE'
        paras = '%d' % (rate)
        return self.net.send_ok(cmd, paras)

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth:
            DTA_6MHZ
            DTA_7MHZ
            DTA_8MHZ
        :return:
        """
        cmd = 'DTA:BANDWIDTH'
        paras = '%d' % (bandwidth)
        return self.net.send_ok(cmd, paras)

    def set_output_level(self, dbm):
        """
        :param dbm:
        QAM : -35.0~0 dBm
        OFDM, ISDB-T : -38.0~-3 dBm
        :return:
        """
        cmd = 'DTA:LEVEL'
        paras = '%d' % (dbm)
        return self.net.send_ok(cmd, paras)

    def set_dvbs(self, type, freq, symbol_rate='27500', code_rate=None):
        """
        init the DVBS/DVBS2 modulation
        :param freq: RF output frequency(Hz)
        :param type: modulation type, like following:
            DTA_DVBS_QPSK
            DTA_DVBS2_QPSK
            DTA_DVBS2_8PSK
        :param symbol_rate: symbol rate in bd
        :param code_rate:
            DTA_1_2
            DTA_2_3
            DTA_3_4
            DTA_4_5
            DTA_5_6
            DTA_6_7
            DTA_7_8
        """

        if code_rate is None:
            code_rate = self.DTA_2_3

        cmd = 'DTA:SET_DVBS'
        paras = '%s %s %s %s' % (type, freq, symbol_rate, code_rate)
        return self.net.send_ok(cmd, paras)

    def set_dvbc(self, type, freq, annex, symbol_rate='6875'):
        """
        init the QAM modulation
        the parameters refer to the play_dvbt function
        :param type: modulation type, like following:
            DTA_QAM4
            DTA_QAM16
            DTA_QAM32
            DTA_QAM64
            DTA_QAM128
            DTA_QAM256
        :param freq: RF output frequency(KHz)
        :param annex:
        DTA_J83_A (DVB-C)
        DTA_J83_B (QAM-B)
        DTA_J83_C (QAM-C)
        :param symbol_rate: symbol rate in Kbd
        """
        cmd = 'DTA:SET_DVBC'
        paras = '%s %s %s %s' % (type, freq, annex, symbol_rate)
        return self.net.send_ok(cmd, paras)

    def set_dvbt(self, type, freq, bandwidth=None, code_rate=None):
        """
        init the DVBT/DVBT2/DTMB/ISDB/ modulation
        :param type: modulation type, like following:
            DTA_DVBT
            DTA_DVBT2
        :param freq: modulation carrier frequency in KHz
        :param bandwidth:
            DTA_6MHZ
            DTA_7MHZ
            DTA_8MHZ
        :param code_rate: Convolutional rate
            DTA_1_2
            DTA_2_3
            DTA_3_4
            DTA_5_6
            DTA_7_8
        :return:
        """

        if bandwidth is None:
            bandwidth = self.DTA_8MHZ
        if code_rate is None:
            code_rate = self.DTA_2_3
        cmd = 'DTA:SET_DVBT'
        if type == self.DTA_DVBT2:
            return False
        paras = '%s %s %s %s' % (type, freq, bandwidth, code_rate)
        return self.net.send_ok(cmd, paras)

    def set_file(self, file, flag=-1):
        """
        select the file of stream
        :param file: the name of stream
        :param flag: -1 = looping,
                     0  = once,
        :return:
        """
        # self.net.send_data("DTA:PLAY")

        cmd = 'DTA:FILE'
        paras = '%s %d' % (file, flag)
        return self.net.send_ok(cmd, paras)

    def set_remux(self, flag):
        """
        set remux for insert the null package.
        :param flag:
            DTA_FALSE
            DTA_TRUE
        """
        cmd = 'DTA:REMUX'
        paras = '%d' % flag
        return self.net.send_ok(cmd, paras)

    def play(self):
        """
        play the stream
        """
        cmd = 'DTA:PLAY'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def pause(self):
        """
        pause the stream
        """
        cmd = 'DTA:PAUSE'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def stop(self):
        """
        stop play the stream
        """
        cmd = 'DTA:STOP'
        paras = ''
        return self.net.send_ok(cmd, paras)

    def rf_enabled_on_stop(self):
        """
        rf enabled on stop
        """
        cmd = ':DTA:RF_ENABLED_ON_STOP 1'
        rec_dta = self.net.send_rec(cmd + "\r\n")
        assert rec_dta == ":DTA:RF_ENABLED_ON_STOP SUCCESS"

    def rf_disabled_on_stop(self):
        """
        rf disabled on stop
        """
        cmd = ':DTA:RF_ENABLED_ON_STOP 0'
        rec_dta = self.net.send_rec(cmd + "\r\n")
        assert rec_dta == ":DTA:RF_ENABLED_ON_STOP SUCCESS"

    def get_stream_total_time(self):
        """
        get stream total time
        """
        cmd = ':DTA:TOTAL_TIME 1\r\n'
        recv_data = self.net.send_rec(cmd)
        try:
            total_time = recv_data[16:]
            print total_time
            return float(total_time)
        except:
            print "get_total_time format err"
            return None

    def get_stream_relative_position(self):
        """
        get stream relative position
        """
        cmd = ':DTA:RELATIVE_POSITION 1\r\n'
        recv_data = self.net.send_rec(cmd)
        try:
            relative_position = recv_data[23:]
            print relative_position
            return float(relative_position)
        except:
            print "get_stream_relative_position format err"
            return None


def _test_set_dvbs():
    print "ekt_test_dvbs start."
    host = '192.168.1.188'
    port = 8900
    net = ekt_net.EktNetClient(host, port)
    dt = EktDtDevice(net)
    dt.set_file('Y:\Customer\HKC\DXD7015\FTV-24May2017.ts', -1)
    dt.set_dvbs(EktDtDevice.DTA_DVBS_QPSK, '1750000', '33000')
    dt.play()
    time.sleep(5)
    dt.set_remux(EktDtDevice.DTA_FALSE)
    time.sleep(5)
    dt.set_freq(1560000)
    time.sleep(5)
    dt.set_sym_rate(28000)
    time.sleep(5)
    dt.set_output_level(-20)
    time.sleep(5)
    dt.set_dvbs(EktDtDevice.DTA_DVBS2_8PSK, '1250000', '26000', EktDtDevice.DTA_5_6)
    time.sleep(5)
    dt.pause()
    time.sleep(5)
    dt.stop()


def _air_download(filename, img, timeout=0):
    """

    :param filename:
    :param img:
    :param timeout:
    :return:
    """
    stream_file = r'D:\Temporary\V5Stream\%s' % filename
    print "ekt_test_dvbs start."
    host = '127.0.0.1'
    port = 8900
    net = ekt_net.EktNetClient(host, port)
    dt = EktDtDevice(net)
    dt.set_file(stream_file, -1)
    dt.set_dvbc(EktDtDevice.DTA_QAM256, '457000', EktDtDevice.DTA_J83_B)
    dt.play()

    # time.sleep(10)
    # stream_file = r'D:\Temporary\V5Stream\SAMEVERSION.ts'
    # dt.set_file(stream_file, -1)
    # dt.set_dvbc(EktDtDevice.DTA_QAM64, 330000, EktDtDevice.DTA_J83_A)
    pass


if __name__ == '__main__':
    # _air_download("SAMEVERSION.ts", "")
    host = '127.0.0.1'
    port = 8900
    net = ekt_net.EktNetClient(host, port)
    dt = EktDtDevice(net)
    dt.get_stream_total_time()
    # dt.set_freq(1560000)
    # dt.set_dvbs(EktDtDevice.DTA_DVBS_QPSK, '1750000', '33000')
    # dt.get_stream_relative_position()

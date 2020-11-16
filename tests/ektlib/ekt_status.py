"""
    Gets the status of the automatic test board
    Author: ivan.zhao@ekt-digital.com
    data: 2020-7-27
"""
import time
import ekt_net


class EktStatus(object):
    """
    Gets the status of the automatic test board
    """

    def __init__(self, net):
        self.net = net

    def get_all_status(self):
        """
        Press key1 and release immediately
        :return:
        """
        count_num = 0
        while True:
            if count_num <= 5:
                cmd = ':RDSP:STB_HW_DATA\r\n'
                self.net.send_data(cmd)
                rec_data_first = self.net.rec_data()
                rec_data_second = self.net.rec_data()

                list_rec_data_first = []
                list_rec_data_second = []

                for data_first in rec_data_first:
                    list_rec_data_first.append(hex(ord(data_first))[2:].rjust(2, '0'))
                for data_second in rec_data_second:
                    list_rec_data_second.append(hex(ord(data_second))[2:].rjust(2, '0'))
                if list_rec_data_first[18] == "04" and list_rec_data_second[18] == "02":
                    list_rec_data_except = list_rec_data_first
                    list_rec_data_7sep_led = list_rec_data_second
                    return list_rec_data_except, list_rec_data_7sep_led
                elif list_rec_data_first[18] == "02" and list_rec_data_second[18] == "04":
                    list_rec_data_except = list_rec_data_second
                    list_rec_data_7sep_led = list_rec_data_first
                    return list_rec_data_except, list_rec_data_7sep_led
                else:
                    print list_rec_data_first
                    print list_rec_data_second
                    # assert False
                    print "Twice the data is not in the required format"
                    count_num = count_num + 1

    def get_lnb_power(self):
        """
        get lnb power : 13v/18v
        :return:float float_lnb_power
        """
        list_rec_data_except, _ = self.get_all_status()
        high_eight = bin(int(list_rec_data_except[19], 16))[2:].rjust(8, '0')
        low_eight = bin(int(list_rec_data_except[20], 16))[2:].rjust(8, '0')
        all_data = "0b" + high_eight + low_eight
        float_lnb_power = int(all_data, 2) / 1000.0
        print float_lnb_power
        return float_lnb_power

    def get_22k_status(self):
        """
        Press key3 and release immediately
        :return:
        """
        list_rec_data_except, _ = self.get_all_status()
        status_22k_bit = list_rec_data_except[21]
        if status_22k_bit == "00":
            status_22k = "not available"
        elif status_22k_bit == "01":
            status_22k = "off"
        elif status_22k_bit == "02":
            status_22k = "on"
        else:
            status_22k = "22k format err"
        print status_22k
        return status_22k

    def get_left_channel_level(self):
        """
        get left channel level
        unit : mV
        :return:
        """
        list_rec_data_except, _ = self.get_all_status()
        print list_rec_data_except[23]
        print list_rec_data_except[24]
        return list_rec_data_except[23], list_rec_data_except[24]

    def get_right_channel_level(self):
        """
        get left channel level
        unit : mV
        :return:
        """
        list_rec_data_except, _ = self.get_all_status()
        print list_rec_data_except[25]
        print list_rec_data_except[26]
        return list_rec_data_except[25], list_rec_data_except[26]

    def get_7sep_status(self):
        """
        get 7sep status
        D0~D6 : a b c d e f g
        boot: 01111100 01011100 01011100 01111000
        :return:sep_0_status
        """
        _, list_rec_data_7sep_led = self.get_all_status()
        sep_0_status = list_rec_data_7sep_led[27]
        sep_1_status = list_rec_data_7sep_led[28]
        sep_2_status = list_rec_data_7sep_led[29]
        sep_3_status = list_rec_data_7sep_led[30]

        sep_0_bin_status = bin(int(sep_0_status, 16))[2:].rjust(8, '0')
        sep_1_bin_status = bin(int(sep_1_status, 16))[2:].rjust(8, '0')
        sep_2_bin_status = bin(int(sep_2_status, 16))[2:].rjust(8, '0')
        sep_3_bin_status = bin(int(sep_3_status, 16))[2:].rjust(8, '0')
        print sep_0_bin_status, sep_1_bin_status, sep_2_bin_status, sep_3_bin_status
        return sep_0_bin_status, sep_1_bin_status, sep_2_bin_status, sep_3_bin_status

    def get_ethernet_status(self):
        """
        get ethernet status
        :return:ethernet_status ("ON"/"OFF")
        """
        _, list_rec_data_7sep_led = self.get_all_status()
        status = list_rec_data_7sep_led[31]
        ethernet_status_bit = bin(int(status, 16))[2:].rjust(8, '0')[1]
        ethernet_status = None
        if ethernet_status_bit == "0":
            ethernet_status = "OFF"
        elif ethernet_status_bit == "1":
            ethernet_status = "ON"
        print ethernet_status
        return ethernet_status

    def get_led_light_status(self):
        """
        get red light status
        :return:
        """
        _, list_rec_data_7sep_led = self.get_all_status()
        status = list_rec_data_7sep_led[31]
        red_status_bit = bin(int(status, 16))[2:].rjust(8, '0')[2]
        green_status_bit = bin(int(status, 16))[2:].rjust(8, '0')[3]
        if red_status_bit == "0" and green_status_bit == "1":
            led_light_status = "green"
        elif red_status_bit == "1" and green_status_bit == "0":
            led_light_status = "red"
        elif red_status_bit == "0" and green_status_bit == "0":
            led_light_status = "off"
        else:
            led_light_status = "unknow status"
        print led_light_status
        return led_light_status

    def get_av_formate_frequency_status(self):
        """
        get av formate frequency status
        001: NTSC-MJ
        010: PAL-BDGHIN
        011: PAL-M
        100: PAL-Combination-N
        101: NTSC4.43
        110: SECAM
        111: CVBS testing not supported or GM7150 init failed
        :return:
        """
        list_rec_data_except, _ = self.get_all_status()
        print list_rec_data_except
        status = list_rec_data_except[31]
        av_frequency_status_bit = bin(int(status, 16))[2:].rjust(8, '0')[4]
        av_formate_status_bit = bin(int(status, 16))[2:].rjust(8, '0')[5:]
        dict_bit_status = {
            "000": "no CVBS",
            "001": "NTSC-MJ",
            "010": "PAL-BDGHIN",
            "011": "PAL-M",
            "100": "PAL-Combination-N",
            "101": "NTSC4.43",
            "110": "SECAM",
            "111": "CVBS testing not supported or GM7150 init failed",
        }
        av_formate_status = dict_bit_status.get(av_formate_status_bit)
        if av_formate_status_bit == "000" or av_formate_status_bit == "111":
            av_frequency_status = "Data nonsense"
        else:
            if av_frequency_status_bit == "0":
                av_frequency_status = "60HZ"
            elif av_frequency_status_bit == "1":
                av_frequency_status = "50HZ"
            else:
                av_frequency_status = "err"
        print av_formate_status
        print av_frequency_status
        return av_formate_status, av_frequency_status

    def __del__(self):
        del self.net


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8900
    net = ekt_net.EktNetClient(host, port)

    # start_time = time.time()
    stat = EktStatus(net)
    # stat.get_ethernet_status()
    # stat.get_led_light_status()
    stat.get_22k_status()
    # stat.get_lnb_power()
    # stat.get_22k_status()
    # stat.get_7sep_status()
    # end_time = time.time()
    # print end_time - start_time

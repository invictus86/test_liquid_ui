"""
    Gets the status of the automatic test board
    Author: ivan.zhao@ekt-digital.com
    data: 2020-7-27
"""
import time
import ekt_net
import ekt_status
import stbt


class EktDiseqc(object):
    """
    Gets the status of the automatic test board
    """

    def __init__(self, net):
        self.net = net

    def get_diseqc_info(self):
        """
        get diseqc10 or diseqc 11 info
        :return:
        """
        # cmd = ':RDSP:DISEQC_DATA\r\n'
        # self.net.send_data(cmd)
        stat = ekt_status.EktStatus(self.net)
        stat.get_all_status()
        list_rec_data = []
        Tone_burse = None
        # stbt.press("KEY_OK")
        self.net.rec_data()
        rec_data = self.net.rec_data()
        for data_first in rec_data:
            list_rec_data.append(hex(ord(data_first))[2:].rjust(2, '0'))
        print list_rec_data
        print len(list_rec_data)
        data_len_list = list_rec_data[21:29]
        try:
            index_num = data_len_list.index("01")
            Tone_burse_bit = list_rec_data[29 + index_num * 8]
            print Tone_burse_bit
            if Tone_burse_bit == "00":
                Tone_burse = "BURST A"
            elif Tone_burse_bit == "ff":
                Tone_burse = "BURST B"
        except:
            Tone_burse = None

        combine_data = ""
        for data in list_rec_data:
            combine_data = combine_data + data
        print combine_data
        diseqc_cmd_10_index = combine_data.find("e01038")
        diseqc_cmd_11_index = combine_data.find("e01039")
        if diseqc_cmd_10_index != -1:
            diseqc_cmd_10_data = combine_data[diseqc_cmd_10_index:diseqc_cmd_10_index + 8]
            dict_diseqc_info = {"0": ["1.0", "Sat-A", "Low", "Vertical"],
                                "1": ["1.0", "Sat-A", "High", "Vertical"],
                                "2": ["1.0", "Sat-A", "Low", "Horizontal"],
                                "3": ["1.0", "Sat-A", "High", "Horizontal"],
                                "4": ["1.0", "Sat-B", "Low", "Vertical"],
                                "5": ["1.0", "Sat-B", "High", "Vertical"],
                                "6": ["1.0", "Sat-B", "Low", "Horizontal"],
                                "7": ["1.0", "Sat-B", "High", "Horizontal"],
                                "8": ["1.0", "Sat-C", "Low", "Vertical"],
                                "9": ["1.0", "Sat-C", "High", "Vertical"],
                                "a": ["1.0", "Sat-C", "Low", "Horizontal"],
                                "b": ["1.0", "Sat-C", "High", "Horizontal"],
                                "c": ["1.0", "Sat-D", "Low", "Vertical"],
                                "d": ["1.0", "Sat-D", "High", "Vertical"],
                                "e": ["1.0", "Sat-D", "Low", "Horizontal"],
                                "f": ["1.0", "Sat-D", "High", "Horizontal"]}
            list_diseqc_info = dict_diseqc_info.get(diseqc_cmd_10_data[-1])
            return list_diseqc_info, Tone_burse
        elif diseqc_cmd_11_index != -1:
            diseqc_cmd_11_data = combine_data[diseqc_cmd_11_index:diseqc_cmd_11_index + 8]
            dict_diseqc_info = {"0": ["1.1", "Sat 1"],
                                "1": ["1.1", "Sat 2"],
                                "2": ["1.1", "Sat 3"],
                                "3": ["1.1", "Sat 4"],
                                "4": ["1.1", "Sat 5"],
                                "5": ["1.1", "Sat 6"],
                                "6": ["1.1", "Sat 7"],
                                "7": ["1.1", "Sat 8"],
                                "8": ["1.1", "Sat 9"],
                                "9": ["1.1", "Sat 10"],
                                "a": ["1.1", "Sat 11"],
                                "b": ["1.1", "Sat 12"],
                                "c": ["1.1", "Sat 13"],
                                "d": ["1.1", "Sat 14"],
                                "e": ["1.1", "Sat 15"],
                                "f": ["1.1", "Sat 16"]}
            list_diseqc_info = dict_diseqc_info.get(diseqc_cmd_11_data[-1])
            return list_diseqc_info, Tone_burse
        else:
            print "diseqc formate err"

    # def __del__(self):
    #     del self.net


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8900
    net = ekt_net.EktNetClient(host, port)
    # net.set_timeout(5)
    # stat = ekt_status.EktStatus(net)
    # stat.get_all_status()

    dis = EktDiseqc(net)
    list_diseqc_info, Tone_burse = dis.get_diseqc_info()
    print list_diseqc_info
    print Tone_burse
    # list_diseqc_info10, Tone_burse, list_diseqc_info_11 = dis.get_diseqc_info_connect_10_11()
    # print list_diseqc_info10
    # print Tone_burse
    # print list_diseqc_info_11

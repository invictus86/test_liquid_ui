"""
    DSN5414a General loader test
    Author: ivan.zhao@ekt-digital.com
    data: 2020-7-14
"""
import os
import sys
import socket
from socket import *
import json

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

from dsn5414a import v5utils
from ektlib import ekt_rds
from ektlib import ekt_dta
from ektlib import ekt_file
from ektlib import ekt_net
from ektlib import ekt_mod
from ektlib import ekt_button, ekt_status
from dsn5414a.v5utils import net
from dsn5414a.v5utils import dvb_type

import time
import stbt
import os


def sys_init():
    """
    init the system,establish connect to the ATserver.
    :return: rds(EKTRds instance),doc(EktFileCfg instance),dta(EktDtDevice instance)
    """
    rds = ekt_rds.EktRds(net)
    dta = ekt_dta.EktDtDevice(net)
    doc = ekt_file.EktFileCfg(net)
    return rds, doc, dta


def ota_init(ts_file, dvb_type=dvb_type):
    """
    read configuration file from ATserver ,then configure the stream server,then play the given ts_file.
    :param ts_file:str,the name of ts file to play
    :param dvb_type: str,the type of the STB under test
    :return:rds(EKTRds instance),doc(EktFileCfg instance),dta(EktDtDevice instance)
    """
    rds, doc, dta = sys_init()
    dta.stop()
    dta.set_file(doc.ts_file(ts_file), -1)
    if dvb_type == '0':
        dta.set_dvbs(doc.config['OTATYPE'], doc.config['OTAFREQ'],
                     code_rate=doc.config['OTACODERATE'])
    if dvb_type == '6':
        dta.set_dvbc(doc.config['OTATYPE'], doc.config['OTAFREQ'],
                     doc.config['OTAANNEX'])
    dta.play()
    return rds, doc, dta



# press operator API
def mult_press(key, count):
    """
    press a key for the given times
    :param key: str,the key to press
    :param count: int,the times to press the key
    :return: None
    """
    for _ in range(count):
        time.sleep(1)
        stbt.press(key)
    time.sleep(1)


def copyfile_to_usb(filename):
    """
    copyfile from computer to usb
    :param key: str,the key to press
    :param filename: str,the bin file name
    :return:
    """
    rds, doc, _ = v5utils.v5_sys_init()
    src_file = doc.cd5_file(filename)
    dst_file = doc.usb_file(doc.load_file)
    print src_file
    print dst_file

    rds.usb_switch_pc()
    time.sleep(8)
    doc.copy_file(src_file, dst_file)
    time.sleep(6)
    rds.usb_switch_stb()
    return rds


def startup_to_dvt_menu():
    """
    reboot the STB if it is not in the DVT APP menu
    :return: None
    """
    rds, _, _ = v5utils.v5_sys_init()
    try:
        v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["menu"], 5)
    except:
        rds.power_off()
        time.sleep(2)
        rds.power_on()
        time.sleep(20)
        v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["menu"], 30)
    return rds


def usb_upgrade_file(filename, match_info, wait_time=0, timeout_secs=300):
    """
    upgrade the given bin file via usb,then check the result
    :param filename: str,bin file name
    :param match_info: list,the texts to be matched
    :param wait_time: int,sleep time before match
    :param timeout_secs: the during time to match the texts
    :return: None
    """
    startup_to_dvt_menu()
    v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["dsn_version_1000"], 5)
    rds = copyfile_to_usb(filename)
    stbt.press("KEY_DOWN")
    time.sleep(0.5)
    mult_press("KEY_OK", 2)
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    rds.usb_switch_none()
    return rds


def usb_upgrade_file_fail(filename, wait_time=0, timeout_secs=300):
    """
    upgrade the given bin file via usb,then check the result
    :param filename: str,bin file name
    :param match_info: list,the texts to be matched
    :param wait_time: int,sleep time before match
    :param timeout_secs: the during time to match the texts
    :return: None
    """
    startup_to_dvt_menu()
    v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["dsn_version_1000"], 5)
    rds = copyfile_to_usb(filename)
    stbt.press("KEY_DOWN")
    time.sleep(0.5)
    mult_press("KEY_OK", 2)
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone([v5utils.ocr_info["100%"], v5utils.ocr_info["menu"]], timeout_secs=timeout_secs)
    rds.usb_switch_none()
    upgrade_success_flag = None
    try:
        v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["100%"], timeout_secs=5)
        upgrade_success_flag = True
    except:
        pass
    if upgrade_success_flag is True:
        assert False
    return rds


def usb_engineer_upgrade_file(filename, match_info, wait_time=0, timeout_secs=300):
    """
    engineer upgrade the given bin file via usb,then check the result
    :param filename: str,bin file name
    :param match_info: list,the texts to be matched
    :param wait_time: int,sleep time before match
    :param timeout_secs: the during time to match the texts
    :return: None
    """
    startup_to_dvt_menu()
    v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["dsn_version_1000"], 5)
    rds = copyfile_to_usb(filename)
    stbt.press("KEY_DOWN")
    time.sleep(0.5)
    stbt.press("KEY_OK")
    time.sleep(0.5)
    stbt.press("KEY_DOWN")
    time.sleep(0.5)
    stbt.press("KEY_OK")
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    rds.usb_switch_none()
    return rds


def usb_engineer_upgrade_file_without_dsn_1000(filename, match_info, wait_time=0, timeout_secs=300):
    """
    engineer upgrade the given bin file via usb,then check the result
    :param filename: str,bin file name
    :param match_info: list,the texts to be matched
    :param wait_time: int,sleep time before match
    :param timeout_secs: the during time to match the texts
    :return: None
    """
    startup_to_dvt_menu()
    rds = copyfile_to_usb(filename)
    stbt.press("KEY_DOWN")
    time.sleep(0.5)
    stbt.press("KEY_OK")
    time.sleep(0.5)
    stbt.press("KEY_DOWN")
    time.sleep(0.5)
    stbt.press("KEY_OK")
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    rds.usb_switch_none()
    return rds


def usb_upgrade_file_without_dsn_1000(filename, match_info, wait_time=0, timeout_secs=300):
    """
    upgrade the given bin file via usb,then check the result
    :param filename: str,bin file name
    :param match_info: list,the texts to be matched
    :param wait_time: int,sleep time before match
    :param timeout_secs: the during time to match the texts
    :return: None
    """
    startup_to_dvt_menu()
    rds = copyfile_to_usb(filename)
    stbt.press("KEY_DOWN")
    time.sleep(0.5)
    mult_press("KEY_OK", 2)
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    rds.usb_switch_none()
    return rds


# def menu_ota_upgrade(ts_file, match_info, wait_time=0, timeout_secs=300):
#     """
#     set ota uograde  OTA Mode  is Upgrade and upgrade the given ts file via ota,then check the result
#     :param ts_file: str,the name of the crc error ts file to play
#     :param match_info: list,the texts used to match
#     :param wait_time: sleep time before start match
#     :param timeout_secs: the during time to match the texts
#     :return: None
#     """
#     _, _, dta = v5utils.v5_ota_init(ts_file)
#     startup_to_dvt_menu()
#     v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["dsn_version_1000"], 5)
#     ekt_mod.mult_press("KEY_DOWN", 2)
#     stbt.press("KEY_OK")
#     time.sleep(0.5)
#     stbt.press("KEY_OK")
#     try:
#         v5utils.wait_for_text_match_list_anyone([v5utils.ocr_info["d_s_not_f"], v5utils.ocr_info["d_s_not_f-"]], timeout_secs=30)
#         stbt.press("KEY_OK")
#     except:
#         pass
#     time.sleep(wait_time)
#     v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
#     return dta


def menu_ota_upgrade(ts_file, match_info, wait_time=0, timeout_secs=300):
    """
    set ota uograde  OTA Mode  is Upgrade and upgrade the given ts file via ota,then check the result
    :param ts_file: str,the name of the crc error ts file to play
    :param match_info: list,the texts used to match
    :param wait_time: sleep time before start match
    :param timeout_secs: the during time to match the texts
    :return: None
    """
    _, _, dta = v5utils.v5_ota_init(ts_file)
    startup_to_dvt_menu()
    v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["dsn_version_1000"], 5)
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press("KEY_OK")
    time.sleep(0.5)
    stbt.press("KEY_OK")
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    return dta


def menu_ota_upgrade_without_dsn_1000(ts_file, match_info, wait_time=0, timeout_secs=300):
    """
    set ota uograde  OTA Mode  is Upgrade and upgrade the given ts file via ota,then check the result
    :param ts_file: str,the name of the crc error ts file to play
    :param match_info: list,the texts used to match
    :param wait_time: sleep time before start match
    :param timeout_secs: the during time to match the texts
    :return: None
    """
    _, _, dta = v5utils.v5_ota_init(ts_file)
    startup_to_dvt_menu()
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press("KEY_OK")
    time.sleep(0.5)
    stbt.press("KEY_OK")
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    return dta


def menu_ota_force_upgrade_without_dsn_1000(ts_file, match_info, wait_time=0, timeout_secs=300):
    """
    set ota uograde  OTA Mode  is Upgrade and upgrade the given ts file via ota,then check the result
    :param ts_file: str,the name of the crc error ts file to play
    :param match_info: list,the texts used to match
    :param wait_time: sleep time before start match
    :param timeout_secs: the during time to match the texts
    :return: None
    """
    _, _, dta = v5utils.v5_ota_init(ts_file)
    startup_to_dvt_menu()
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press("KEY_OK")
    time.sleep(0.5)
    ekt_mod.mult_press("KEY_DOWN", 12)
    stbt.press("KEY_RIGHT")
    time.sleep(0.5)
    stbt.press("KEY_OK")
    try:
        v5utils.wait_for_text_match_list_anyone([v5utils.ocr_info["d_s_not_f"], v5utils.ocr_info["d_s_not_f-"]], timeout_secs=30)
        stbt.press("KEY_OK")
    except:
        pass
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    return dta


def menu_ota_upgrade_without_match(ts_file, wait_time=0):
    """
    set ota uograde  OTA Mode  is Upgrade and upgrade the given ts file via ota,then check the result
    :param ts_file: str,the name of the crc error ts file to play
    :param match_info: list,the texts used to match
    :param wait_time: sleep time before start match
    :param timeout_secs: the during time to match the texts
    :return: None
    """
    _, _, dta = v5utils.v5_ota_init(ts_file)
    startup_to_dvt_menu()
    v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["dsn_version_1000"], 5)
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press("KEY_OK")
    time.sleep(0.5)
    stbt.press("KEY_OK")
    time.sleep(wait_time)
    return dta


def v5_menu_ota_set_download_frequency(frequency):
    """
    set OTA download parameters
    :param frequency: str,the download frequency
    :param pid: str,the download PID
    :param doc: an EktFileCfg instance that perform file operation
    :param dvb_type: the type of the STB under test
    :return: None
    """
    _, doc, _ = v5utils.v5_sys_init()
    frequency1 = str(9750 + int(doc.config['OTAFREQ'][:-3])).zfill(5)
    frequency2 = str(5150 + int(doc.config['OTAFREQ'][:-3])).zfill(5)
    dict_data = {
        "09750": frequency1,
        "05150": frequency2
    }
    startup_to_dvt_menu()
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press("KEY_OK")
    time.sleep(1)
    stbt.press("KEY_DOWN")
    time.sleep(1)
    ekt_mod.input_digital(str(frequency))
    time.sleep(1)
    ekt_mod.mult_press("KEY_DOWN", 5)
    time.sleep(1)
    ekt_mod.input_digital(dict_data.get(frequency))
    time.sleep(1)


def set_turning_frequency_ota_upgrade(doc, frequency):
    dict_data = {
        950: ["10600", "11550"],
        1500: ["10600", "12100"],
        1800: ["10600", "12400"],
        2150: ["10600", "12750"]
    }
    startup_to_dvt_menu()
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press("KEY_OK")
    time.sleep(1)
    stbt.press("KEY_DOWN")
    time.sleep(1)
    ekt_mod.input_digital(dict_data[frequency][0])
    time.sleep(1)
    ekt_mod.mult_press("KEY_DOWN", 5)
    time.sleep(1)
    ekt_mod.input_digital(dict_data[frequency][1])
    time.sleep(1)

    # Subsequent to delete
    ekt_mod.mult_press("KEY_DOWN", 2)
    ekt_mod.mult_press("KEY_LEFT", 2)
    ekt_mod.input_digital("27500")
    time.sleep(1)
    ekt_mod.mult_press("KEY_DOWN", 2)

    # ekt_mod.mult_press("KEY_DOWN", 4)
    ekt_mod.input_digital(doc.config['PID'])


def set_symbol_rate_ota_upgrade(symbol_rate):
    dict_data = {
        5000: "00005",
        2000: "00002",
        10000: "00010",
        30000: "00030",
        45000: "00045"
    }
    startup_to_dvt_menu()
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press("KEY_OK")
    time.sleep(1)
    ekt_mod.mult_press("KEY_DOWN", 8)
    ekt_mod.input_digital(dict_data[symbol_rate])


def set_fec_ota_upgrade(fec):
    startup_to_dvt_menu()
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press("KEY_OK")
    time.sleep(1)
    ekt_mod.mult_press("KEY_DOWN", 9)
    count = 0
    while count < 10:
        frame = stbt.get_frame()
        if stbt.ocr(frame, region=v5utils.regions.get("fec")) == fec:
            break
        else:
            stbt.press("KEY_RIGHT")
            time.sleep(5)
            count += 1


def set_pid_area_value():
    startup_to_dvt_menu()
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press("KEY_OK")
    time.sleep(1)
    ekt_mod.mult_press("KEY_DOWN", 10)
    ekt_mod.input_digital("406")
    stbt.press("KEY_DOWN")
    time.sleep(0.5)
    ekt_mod.mult_press("KEY_LEFT", 2)
    ekt_mod.input_digital("01")


def menu_ota_upgrade_flag(ts_file, match_info, wait_time=0, timeout_secs=300, flag=None):
    """
    set ota uograde  OTA Mode  is Upgrade and upgrade the given ts file via ota,then check the result
    :param ts_file: str,the name of the crc error ts file to play
    :param match_info: list,the texts used to match
    :param wait_time: sleep time before start match
    :param timeout_secs: the during time to match the texts
    :return: None
    """
    _, doc, dta = v5utils.v5_ota_init(ts_file)
    if flag == 5:
        set_pid_area_value()
    elif flag == 6:
        set_turning_frequency_ota_upgrade(doc, 950)
        dta.set_freq(950000)
    elif flag == 7:
        set_turning_frequency_ota_upgrade(doc, 1500)
        dta.set_freq(1500000)
    elif flag == 8:
        set_turning_frequency_ota_upgrade(doc, 1800)
        dta.set_freq(1800000)
    elif flag == 9:
        set_turning_frequency_ota_upgrade(doc, 2150)
        dta.set_dvbs(ekt_dta.EktDtDevice.DTA_DVBS_QPSK, 2150000, '27500', code_rate=ekt_dta.EktDtDevice.DTA_2_3)
    elif flag == 10:
        set_symbol_rate_ota_upgrade(5000)
        dta.set_dvbs(ekt_dta.EktDtDevice.DTA_DVBS2_8PSK, doc.config['OTAFREQ'], '5000',
                     code_rate=ekt_dta.EktDtDevice.DTA_2_3)
    elif flag == 11:
        set_symbol_rate_ota_upgrade(10000)
        dta.set_dvbs(ekt_dta.EktDtDevice.DTA_DVBS_QPSK, doc.config['OTAFREQ'], '10000',
                     code_rate=ekt_dta.EktDtDevice.DTA_2_3)
    elif flag == 12:
        set_symbol_rate_ota_upgrade(30000)
        dta.set_dvbs(ekt_dta.EktDtDevice.DTA_DVBS_QPSK, doc.config['OTAFREQ'], '30000',
                     code_rate=ekt_dta.EktDtDevice.DTA_2_3)
    elif flag == 13:
        set_symbol_rate_ota_upgrade(45000)
        dta.set_dvbs(ekt_dta.EktDtDevice.DTA_DVBS_QPSK, doc.config['OTAFREQ'], '45000',
                     code_rate=ekt_dta.EktDtDevice.DTA_2_3)
    elif flag == 14:
        set_fec_ota_upgrade("1/2")
        dta.set_dvbs(ekt_dta.EktDtDevice.DTA_DVBS_QPSK, doc.config['OTAFREQ'], '27500',
                     code_rate=ekt_dta.EktDtDevice.DTA_1_2)
    elif flag == 15:
        set_fec_ota_upgrade("3/4")
        dta.set_dvbs(ekt_dta.EktDtDevice.DTA_DVBS_QPSK, doc.config['OTAFREQ'], '27500',
                     code_rate=ekt_dta.EktDtDevice.DTA_3_4)
    elif flag == 16:
        # set_fec_ota_upgrade("7/8")
        set_fec_ota_upgrade("7/.")
        dta.set_dvbs(ekt_dta.EktDtDevice.DTA_DVBS_QPSK, doc.config['OTAFREQ'], '27500',
                     code_rate=ekt_dta.EktDtDevice.DTA_7_8)
    elif flag == 17:
        set_symbol_rate_ota_upgrade(2000)
        dta.set_dvbs(ekt_dta.EktDtDevice.DTA_DVBS_QPSK, doc.config['OTAFREQ'], '2000',
                     code_rate=ekt_dta.EktDtDevice.DTA_2_3)
    stbt.press("KEY_OK")
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    return dta


def menu_ota_upgrade_forced(ts_file, match_info, wait_time=0, timeout_secs=300):
    """
    set ota uograde  OTA Mode  is forced and upgrade the given ts file via ota,then check the result
    :param ts_file: str,the name of the crc error ts file to play
    :param match_info: list,the texts used to match
    :param wait_time: sleep time before start match
    :param timeout_secs: the during time to match the texts
    :return: None
    """
    _, _, dta = v5utils.v5_ota_init(ts_file)
    startup_to_dvt_menu()
    v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["dsn_version_1000"], 5)
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press("KEY_OK")
    time.sleep(0.5)
    ekt_mod.mult_press("KEY_DOWN", 12)
    stbt.press("KEY_RIGHT")
    time.sleep(0.5)
    stbt.press("KEY_OK")
    try:
        v5utils.wait_for_text_match_list_anyone([v5utils.ocr_info["d_s_not_f"], v5utils.ocr_info["d_s_not_f-"]], timeout_secs=30)
        stbt.press("KEY_OK")
    except:
        pass
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    return dta


def ota_dowdloading_interrupted_15s(ts_file, match_info, wait_time=0):
    """
    while at OTA upgrade process, match the given texts
    :param ts_file: str,the name of the crc error ts file to play
    :param match_info: list,the texts used to match
    :param timeout: sleep time before start match
    :return: None
    """
    _, _, dta = v5utils.v5_ota_init(ts_file)
    startup_to_dvt_menu()
    v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["dsn_version_1000"], 5)
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press("KEY_OK")
    time.sleep(0.5)
    stbt.press("KEY_OK")
    time.sleep(0.5)
    stbt.press("KEY_OK")
    # time.sleep(33)
    v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["download_DDB"], timeout_secs=60)
    dta.stop()
    # time.sleep(12)
    time.sleep(15)
    dta.play()
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info)


def set_data_func(data):
    HOST = '192.168.1.24'
    PORT = 9991
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    json_data = json.dumps(data)
    tcpCliSock.send(json_data.encode("utf-8"))
    rec_data = tcpCliSock.recv(BUFSIZ)
    tcpCliSock.close()
    return rec_data


def match_menu_dsn_version(match_info):
    v5utils.wait_for_text_match_list_anyone(match_info)


def match_module_info_version(module_num, match_info):
    stbt.press("KEY_OK")
    time.sleep(1)
    ekt_mod.mult_press("KEY_RIGHT", module_num)
    v5utils.wait_for_text_match_list_anyone(match_info)
    stbt.press("KEY_EXIT")


def usb_frontpanel_upgrade_file(filename, match_info, wait_time=0, timeout_secs=300):
    """
    upgrade the given bin file via usb usb front panel,then check the result
    :param filename: str,bin file name
    :param match_info: list,the texts to be matched
    :param wait_time: int,sleep time before match
    :param timeout_secs: the during time to match the texts
    :return: rds
    """
    rds = copyfile_to_usb(filename)
    sta = ekt_status.EktStatus(net)
    sta.get_all_status()
    del sta
    btn = ekt_button.EktButton(net)

    rds.power_off()
    time.sleep(3)
    btn.key5_down()
    time.sleep(1)
    rds.power_on()
    time.sleep(5)
    btn.key5_up()
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    rds.usb_switch_none()
    return rds


def ota_front_panel_upgrade_file(ts_file, match_info, wait_time=0, timeout_secs=300):
    """
    set ota uograde  OTA Mode  is Upgrade and upgrade the given ts file via ota,then check the result
    :param ts_file: str,the name of the crc error ts file to play
    :param match_info: list,the texts used to match
    :param wait_time: sleep time before start match
    :param timeout_secs: the during time to match the texts
    :return: None
    """
    rds, _, dta = v5utils.v5_ota_init(ts_file)
    btn = ekt_button.EktButton(net)
    rds.power_off()
    time.sleep(3)
    btn.key5_down()
    time.sleep(1)
    rds.power_on()
    time.sleep(7)
    btn.key5_up()
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["connect"], timeout_secs=30)
    stbt.press("KEY_OK")
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    return dta


def file_usb_before_enter_app(filename, match_info, wait_time=0, timeout_secs=60):
    """
    upgrade via USB before the STB can enter DVT APP
    :param filename:str,CD5 file name
    :param match_info: the texts to be matched
    :param wait_time: sleep time before start match
    :param timeout_secs: the time to match texts
    :return: rds
    """
    rds = copyfile_to_usb(filename)
    rds.power_off()
    time.sleep(5)
    rds.power_on()
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    rds.usb_switch_none()
    return rds


def ota_upgrade_before_dvtapp(ts_file, match_info, wait_time=0, timeout_secs=60):
    """
    set ota uograde  OTA Mode  is Upgrade and upgrade the given ts file via ota,then check the result
    :param ts_file: str,the name of the crc error ts file to play
    :param match_info: list,the texts used to match
    :param wait_time: sleep time before start match
    :param timeout_secs: the during time to match the texts
    :return: dta
    """
    rds, _, dta = v5utils.v5_ota_init(ts_file)
    rds.power_off()
    time.sleep(5)
    rds.power_on()
    time.sleep(wait_time)
    v5utils.wait_for_text_match_list_anyone(match_info, timeout_secs=timeout_secs)
    return dta


def menu_to_ota_upgrade():
    """
    set ota uograde  OTA Mode  is Upgrade and upgrade the given ts file via ota,then check the result
    :return: None
    """
    startup_to_dvt_menu()
    v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["dsn_version_1000"], 5)
    mult_press("KEY_DOWN", 2)
    stbt.press("KEY_OK")
    time.sleep(1)


def menu_to_flsh_dump_da2(usb_dump_folder):
    """
    menu to flsh dump da2
    :return: None
    """
    startup_to_dvt_menu()
    rds, doc, dta = v5utils.v5_sys_init()
    rds.usb_switch_stb()
    time.sleep(3)
    ekt_mod.mult_press("KEY_UP", 2)
    stbt.press("KEY_OK")
    time.sleep(1)
    stbt.press("KEY_DOWN")
    time.sleep(1)
    stbt.press("KEY_OK")
    time.sleep(2)
    ekt_mod.input_digital("00270000")
    time.sleep(1)
    stbt.press("KEY_DOWN")
    time.sleep(1)
    ekt_mod.input_digital("00000900")
    time.sleep(2)
    stbt.press("KEY_DOWN")
    time.sleep(1)
    stbt.press("KEY_OK")
    v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["dump_success"], timeout_secs=10)
    rds.usb_switch_pc()
    time.sleep(8)
    doc.copy_file("F:/flash_dump.bin", "F:/{}/flash_dump.bin".format(usb_dump_folder))
    ekt_mod.mult_press("KEY_EXIT", 2)
    ekt_mod.mult_press("KEY_DOWN", 2)
    rds.usb_switch_none()


def menu_to_flsh_dump_da2_redundant(usb_dump_folder):
    """
    menu to flsh dump da2 redundant
    :return: None
    """
    startup_to_dvt_menu()
    rds, doc, dta = v5utils.v5_sys_init()
    rds.usb_switch_stb()
    time.sleep(3)
    ekt_mod.mult_press("KEY_UP", 2)
    stbt.press("KEY_OK")
    time.sleep(1)
    stbt.press("KEY_DOWN")
    time.sleep(1)
    stbt.press("KEY_OK")
    time.sleep(2)
    ekt_mod.input_digital("00280000")
    time.sleep(1)
    stbt.press("KEY_DOWN")
    time.sleep(1)
    ekt_mod.input_digital("00000900")
    time.sleep(2)
    stbt.press("KEY_DOWN")
    time.sleep(1)
    stbt.press("KEY_OK")
    v5utils.wait_for_text_match_list_anyone(v5utils.ocr_info["dump_success"], timeout_secs=10)
    rds.usb_switch_pc()
    time.sleep(8)
    doc.copy_file("F:/flash_dump.bin", "F:/{}/flash_dump.bin".format(usb_dump_folder))
    ekt_mod.mult_press("KEY_EXIT", 2)
    ekt_mod.mult_press("KEY_DOWN", 2)
    rds.usb_switch_none()

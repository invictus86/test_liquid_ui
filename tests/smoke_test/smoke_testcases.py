#!usr/bin/env python
# !usr/bin/python

import time
import sys
import os
import stbt

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print parentdir
sys.path.insert(0, parentdir)

import ektlib.ekt_relay
from ektlib import ekt_net, ekt_rds, ekt_mod, ekt_dta
from smoke_test import v5utils

# -------------------------Known Issue-------------------------------
# 1. CA temp window may popup and make the test cases fail
# 2. draw_text() doesn't work
# 3. str.isdigit() serial functions don't work
# 4. do not match fram immediately after a key press(it will compare with the old fram)


# global variables(assigned value from outside input)

# the IP and port of ATserver
net = ekt_net.EktNetClient('192.168.1.24', 8900)

g_show_case_name = 'True'

# g_freq = 11650
g_freq_dvbs = 11438
g_freq_dvbc_annexa = 788000
g_freq_dvbt = 722000
# g_symrate = 27500
g_symrate_dvbs = 30000
g_symrate_dvbc_annexa = 6875

g_strict_match_parameters = stbt.MatchParameters(match_method=None, match_threshold=0.95, confirm_method='absdiff',
                                                 confirm_threshold=0.18, erode_passes=None)

g_password = "0000"

g_list_key_num = ['KEY_0', 'KEY_1', 'KEY_2', 'KEY_3', 'KEY_4', 'KEY_5', 'KEY_6', 'KEY_7', 'KEY_8', 'KEY_9']

g_stream_file = r'Y:\Ivan\autotest\smoke_test\QE_7_days_EPG.ts'


# power control
# g_power_relay = ektlib.ekt_relay.EktRelay()
# g_relay_index = 1


# ---------------------------------------------------------
# liquid smoke test entry function
# ---------------------------------------------------------
def test_liquid_smoke_test_dvbs():
    """
    test liquid UI smoke test
    :param frontend: DVB mode
    :return:
    """
    test_liquid_system_restart()
    test_liquid_do_factory_reset()
    test_liquid_manual_channel_search_s()
    test_channel_up(10)


def test_liquid_smoke_test_dvbc_annexa():
    """
    test liquid UI smoke test
    :param frontend: DVB mode
    :return:
    """
    test_liquid_system_restart()
    test_liquid_do_factory_reset()
    test_liquid_manual_channel_search_c_annexa()
    test_channel_up(10)


def test_liquid_smoke_test_dvbt():
    """
    test liquid UI smoke test
    :param frontend: DVB mode
    :return:
    """
    test_liquid_system_restart()
    test_liquid_do_factory_reset()
    test_liquid_manual_channel_search_t()
    test_channel_up(10)


# do Restore Default Settings under menu Personal Settings
def test_liquid_do_factory_reset():
    """
    reset to factory andh check tv list is empty
    :return:
    """
    if g_show_case_name == "True":
        stbt.draw_text("test_liquid_do_factory_reset", 5)
    goto_main_menu()

    ekt_mod.mult_press("KEY_RIGHT", 4)
    ekt_mod.mult_press("KEY_DOWN", 4)
    stbt.press('KEY_OK')
    time.sleep(1)
    stbt.press('KEY_DOWN')
    ekt_mod.mult_press("KEY_OK", 2)
    ekt_mod.input_digital(str(g_password))
    time.sleep(10)
    stbt.wait_for_match('images/liquid/initial_settings.png', 20)
    stbt.press('KEY_EXIT')


# do manual channel search for DVB-s boxes
def test_liquid_manual_channel_search_s():
    """
    channel search for dvb-s
    :return:
    """
    set_stream_xpress_parameter_dvbs()
    if g_show_case_name == "True":
        stbt.draw_text("test_liquid_manual_channel_search_s", 5)

    goto_main_menu()
    ekt_mod.mult_press("KEY_RIGHT", 3)
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press('KEY_OK')

    stbt.press_until_match('KEY_DOWN', 'images/liquid/antenna_lnb_freq_field.png')
    stbt.press_until_match('KEY_RIGHT', 'images/liquid/antenna_lnb_freq_9750.png', match_parameters=g_strict_match_parameters)

    time.sleep(1)
    stbt.press('KEY_OK')
    ekt_mod.mult_press("KEY_DOWN", 3)
    stbt.press('KEY_OK')

    # add a new TP
    # perform several times in case popup window will make the test failure
    n = 0
    while n < 3:
        stbt.press('KEY_GREEN')
        stbt.wait_for_match('images/liquid/antenna_add_tp.png')
        ekt_mod.input_digital(str(g_freq_dvbs))
        stbt.press('KEY_DOWN')
        time.sleep(1)
        ekt_mod.input_digital(str(g_symrate_dvbs))
        stbt.press('KEY_OK')
        time.sleep(3)
        if stbt.match('images/liquid/antenna_ssi_sqi_lock.png'):
            break
        n += 1
    assert n < 3

    # TP manual search
    stbt.press('KEY_BLUE')
    stbt.wait_for_match("images/liquid/antenna_tp_search.png", timeout_secs=5)
    stbt.press('KEY_OK')
    time.sleep(5)
    stbt.wait_for_match("images/liquid/tp_search_scan_end.png", timeout_secs=10)
    stbt.press('KEY_OK')

    stbt.wait_for_motion(20)
    ekt_mod.mult_press("KEY_LEFT", 15)


# do manual channel search for DVB-c boxes
def test_liquid_manual_channel_search_c_annexa():
    """
    channel search for dvb-c annexa
    :return:
    """
    set_stream_xpress_parameter_dvbc_annexa()
    if g_show_case_name == "True":
        stbt.draw_text("test_liquid_manual_channel_search_c_annexa", 5)

    goto_main_menu()
    ekt_mod.mult_press("KEY_RIGHT", 3)
    stbt.press('KEY_OK')
    time.sleep(1)
    ekt_mod.mult_press("KEY_0", 4)
    ekt_mod.mult_press("KEY_Left", 6)
    ekt_mod.input_digital(str(int(g_freq_dvbc_annexa)))
    stbt.press('KEY_Down')
    time.sleep(0.5)
    ekt_mod.mult_press("KEY_Left", 4)
    ekt_mod.input_digital(str(g_symrate_dvbc_annexa))
    ekt_mod.mult_press("KEY_Down", 3)
    time.sleep(5)
    try:
        stbt.wait_for_match("images/liquid/dvbc_annexa/annexa_strength_success.png", timeout_secs=10)
    except:
        stbt.wait_for_match("images/liquid/dvbc_annexa/annexa_strength_fail.png", timeout_secs=10)
        print "lock table fail"
        assert False
    stbt.press('KEY_OK')
    stbt.wait_for_match("images/liquid/dvbc_annexa/annexa_tv_4.png", timeout_secs=20)
    stbt.press('KEY_OK')

    stbt.wait_for_motion(20)
    ekt_mod.mult_press("KEY_LEFT", 15)


# do manual channel search for DVB-t boxes
def test_liquid_manual_channel_search_t():
    """
    channel search for dvb-t annexa
    :return:
    """
    bandwidth = 8
    set_stream_xpress_parameter_dvbt()
    if g_show_case_name == "True":
        stbt.draw_text("test_liquid_manual_channel_search_t", 5)

    goto_main_menu()
    ekt_mod.mult_press("KEY_RIGHT", 3)
    stbt.press('KEY_DOWN')
    time.sleep(0.5)
    stbt.press('KEY_OK')
    time.sleep(0.5)
    stbt.press('KEY_RIGHT')
    time.sleep(0.5)
    stbt.press('KEY_DOWN')
    time.sleep(0.5)
    ekt_mod.mult_press("KEY_LEFT", 3)
    ekt_mod.input_digital(str(int(g_freq_dvbt))[:3])
    stbt.press('KEY_DOWN')
    time.sleep(0.5)
    for _ in range(10):
        frame = stbt.get_frame()
        print stbt.ocr(frame, region=v5utils.regions.get("bandwidth"))
        if stbt.ocr(frame, region=v5utils.regions.get("bandwidth")) == "{}M".format(str(bandwidth)):
            break
        else:
            stbt.press("KEY_RIGHT")
            time.sleep(0.5)
    ekt_mod.mult_press("KEY_DOWN", 2)
    stbt.press('KEY_OK')
    stbt.wait_for_match("images/liquid/tp_search_scan_end.png", timeout_secs=10)
    stbt.press('KEY_OK')

    stbt.wait_for_motion(20)
    ekt_mod.mult_press("KEY_LEFT", 15)


# do channel up
def test_channel_up(count=1):
    """
    channel up and check for screen is moving
    :param count:
    :return:
    """
    i = 0
    print "count = ", count

    while i < count:
        stbt.press('KEY_UP', 2)
        i += 1
        stbt.wait_for_motion(10)


# do channel down
def test_channel_down(count=1):
    """
    channel down and check for screen is moving
    :param count:
    :return:
    """
    i = 0
    print "count = ", count

    while i < count:
        stbt.press('KEY_DOWN', 2)
        i += 1
        stbt.wait_for_motion(10)


# system starts up
def test_liquid_system_restart():
    """
    power of the stb
    check screen is blach
    power on the stb
    check for the menu screen
    :return:
    """
    # power down
    test_system_power_down()

    # confirm HDMI has no output in 15s
    timewait = 0
    while not stbt.is_screen_black():
        time.sleep(5)
        timewait += 5
        assert timewait < 15

    # power up
    test_system_power_up()

    # at least wait for 30s
    time.sleep(30)

    # skip boot logo & first time installation if any(Exit key?)
    # confirm main menu will appear in 180s
    timewait = 0
    while not stbt.match('images/liquid/main_memu.png'):
        stbt.press('KEY_EXIT')
        stbt.press('KEY_EXIT')
        stbt.press('KEY_EXIT')
        stbt.press('KEY_EXIT')
        stbt.press('KEY_MENU')

        time.sleep(5)
        timewait += 5
        assert timewait < 180


def test_system_power_down():
    """
    power off the stb
    :return:
    """
    print(sys.version)
    rds = ekt_rds.EktRds(net)
    rds.power_off()
    # g_power_relay.relay_off(g_relay_index)


def test_system_power_up():
    """
    power on the stb
    :return:
    """
    rds = ekt_rds.EktRds(net)
    rds.power_on()
    # g_power_relay.relay_on(g_relay_index)


# -------------------------------------------------------
# common used internal functions defined here
# -------------------------------------------------------

def goto_main_menu():
    """
    go to the main menu in any interface
    :return:
    """
    stbt.press('KEY_MENU')
    time.sleep(1)
    stbt.press('KEY_EXIT')
    time.sleep(1)
    stbt.press_until_match('KEY_MENU', 'images/liquid/main_memu.png')


def set_stream_xpress_parameter_dvbs():
    """
    set stream file, dvb mode, frequency, symbol rate
    :return:
    """
    dt = ekt_dta.EktDtDevice(net)
    dt.set_device(107, 5)
    time.sleep(1)
    dt.set_file(g_stream_file, -1)
    time.sleep(1)
    dt.set_dvbs(ekt_dta.EktDtDevice.DTA_DVBS_QPSK, str(g_freq_dvbs - 9750) + "000", str(g_symrate_dvbs), ekt_dta.EktDtDevice.DTA_3_4)
    time.sleep(1)
    dt.play()


def set_stream_xpress_parameter_dvbc_annexa():
    """
    set stream file, dvb mode, frequency, symbol rate
    :return:
    """
    dt = ekt_dta.EktDtDevice(net)
    dt.set_device(115, 1)
    time.sleep(1)
    dt.set_file(g_stream_file, -1)
    time.sleep(1)
    dt.set_dvbc(ekt_dta.EktDtDevice.DTA_QAM64, str(g_freq_dvbc_annexa)[:3], ekt_dta.EktDtDevice.DTA_J83_A,
                symbol_rate=str(g_symrate_dvbc_annexa))
    time.sleep(1)
    dt.set_freq(g_freq_dvbc_annexa)
    time.sleep(1)
    dt.play()


def set_stream_xpress_parameter_dvbt():
    """
    set stream file, dvb mode, frequency, symbol rate
    :return:
    """
    dt = ekt_dta.EktDtDevice(net)
    dt.set_device(115, 7)
    time.sleep(1)
    dt.set_file(g_stream_file, -1)
    time.sleep(1)
    dt.set_dvbt(ekt_dta.EktDtDevice.DTA_DVBT, str(g_freq_dvbt)[:3], ekt_dta.EktDtDevice.DTA_8MHZ, ekt_dta.EktDtDevice.DTA_1_2)
    dt.set_freq(g_freq_dvbt)
    time.sleep(1)
    dt.play()


def test_only_test():
    stbt.wait_for_match("images/liquid/dvbc_annexa/annexa_tv_4.png", timeout_secs=20)
    # frame = stbt.get_frame()
    # print stbt.ocr(frame, region=v5utils.regions.get("bandwidth"))
    # set_stream_xpress_parameter_dvbt()

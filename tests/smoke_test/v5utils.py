"""
    DSN7414v General loader test
    Author: ivan.zhao@ekt-digital.com
    data: 2019-10-17

"""
import time
import os
import sys
import re
import stbt

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

from ektlib import ekt_rds
from ektlib import ekt_file
from ektlib import ekt_net
from ektlib import ekt_mod
from ektlib import ekt_dta

# global parameters
# the IP and port of ATserver

# get dvb_type from ATserver configuration file

# the time box takes to start up
start_up_time = 40

# ota download timeout time plus acceptable bias time(s)
ota_timeout_time = 180 + 10

# path = {'0':"dvb_s_images/",'6':"images/"}
# img_path = path[dvb_type]

# texts to be matched
texts = {
    # "menu": "DVT Test Application",
    "menu": "DVT",
    "0x80000D06": "0x80000D06",
    "0x80000D06-": "0x80000006",
    "0x80000D20": "0x80000D20",
    "0x80000D20-": "0x80000020",
    "0x80000D21": "0x80000021",
    "0x80000D07": "0x80000D07",
    "0x80000D07-": "0x80000007",
    "0x80000D0D": "0x80000000",
    "0x80000D0D-": "0x80000DOD",
    "0x80000D0D--": "OXBOOOODOD",
    "0x80000C0A": "0x80000COA",
    "0x80000C0A-": "0x80000COA",
    "0x80000C0A--": "OXBOOOOCOA",
    "0x80000C0A---": "0x8000OCOA",
    "0x80030031": "0x80030031",
    "0x80030038": "0x80030038",
    "0x80030003": "0x80030003",
    "0x80001300": "0x80001 300",
    "0x80001300-": "0x80001300",
    "0x80000D02": "0x80000002",
    "0x80000D30": "0x80000030",
    "0x80000D41": "0x80000041",
    "loader_err_code": "error: 30003",
    "1.20": "1.20",
    "20000": "20000",
    "100%": "100%",
    "75%": "75%",
    "70%": "70%",
    "download_usb": "Download USB",
    "salvando": "Salvando",
    "programming_flash": "Programming flash...",
    "ok": "OK",
    "start": "START",
    "comecar": "COMECAR",
    "plase_choose": "Please choose the network connection to upgrade...",
    "balxando_dados": "Balxando dados...",
    "analyzing_upgrade_file": "Analyzing upgrade llle...",
    "downloading_data": "Downloading data...",
    "upgrade": "Upgrade",
    "forced": "Forced",
    "d_s_f": "Download Service Found",
    "d_s_not_f": "Download Service Not Found",
    "download_DDB": "Downloading DDB",
    "download_dsi": "DOWNLOADING DSIIDII",
    "loading_data": "Loadlng Data  M1 of 3",
    "process_m1": "Processlng data  M1 of 3",
    "process_m2": "Processlng data  M2 of 3",
    "process_m3": "Processlng data  M3 of 3",
    "signature_error": "Slgnature verlflcatlon has falled.",
    "erase_irdeto": "Status :lrdetoPartition Successfully Erased",
    "erase_CA": "Status :CAPartition Successfully Erased",
    "erase_loader": "Status :LoaderPartition Successfully Erased",
    "erase_all": "Status :Entire Partition Successfully Erased",
    "reset_to_default": "Status :Reset To Defaults Successful",
    "bE1": " bE1 Boot check error",
    "hide_loaderinfo": "Status: Set Hide Loaderlnfo successful",
    "set_bootcheck": "Status: Set BootCheckMode successful",
    "set_OSD_hide": "Status: Set OSD Hide Mode successful",
    "usb_upgrade": "USB Upgrade",
    "status": "Status: Tuna tall.",
    "config": "Configure DVB-S/SZ",
    "loader_menu": "Press 'OK' to show system information",
    "run_loader": "run loader...",
    "run_app": "run app...",
    "serial_number": "Status: thto Sorlal Number successful",
    "12345678": "12345678",
    "av_output_result": "Status: Disable Loader vldoo output success.",
    "manufacture_code": "Manufacture Code:",
    "manufacture_name": "Manufacture Name:",
    "model": "Model:",
    "hw_version": "HW Version:",
    "app_version": "APP Version:",
    "loader_version": "Loader Version:",
    "boot_logo_version": "Boot Logo Version:",
    "loader_res_version": "Loader Res Version:",
    "russian_err_message": "He yAaJ'IOCb aarpyamb AaHHble Ann I'IO. ..",
    "spanish_err_message": "Tiempo de uso",
    "set_language_flag": "Status: Set 080 language successful.",
    "dsn_version_1001": "1001",
    "dsn_version_1000": "1000",
    "dsn_version_1100": "1100",
    "dsn_version_1101": "1101",
    "dsn_version_1102": "1102",
    "dsn_version_1103": "1103",
    "dsn_version_1104": "1104",
    "module_version_1001": "1001",
    "module_version_1000": "1000",
    "module_version_1100": "1100",
    "module_version_1101": "1101",
    "module_version_1102": "1102",
    "module_version_1103": "1103",
    "module_version_1104": "1104",
    "loader_dsn": "DSN:",
    "loader_man_code": "MAN CODE:",
    "loader_model_code": "MODEL NAME:",
    "loader_hw_ver": "HW VER:",
    "loader_loader_ver": "LOADER VER:",
    "loader_key_ver": "KEY VER:",

}

# regions the text to be matched
regions = {

    "1.20": stbt.Region(221, 123, right=256, bottom=137),
    "20000": stbt.Region(220, 123, right=273, bottom=137),
    "dsn_region": stbt.Region(267, 427, right=317, bottom=460),
    "dsn": stbt.Region(80, 424, right=342, bottom=470),
    "module_version": stbt.Region(789, 342, right=912, bottom=385),
    "error_code": stbt.Region(117, 561, right=318, bottom=608),
    "error_info": stbt.Region(122, 622, right=766, bottom=678),
    "download_process": stbt.Region(487, 537, right=811, bottom=585),
    "ISIGN_Ver": stbt.Region(84, 498, right=346, bottom=532),
    "Key_Sys_ID": stbt.Region(666, 428, right=928, bottom=462),
    "progress_time": stbt.Region(728, 560, right=966, bottom=609),
    "progress_bar_status": stbt.Region(1061, 510, right=1159, bottom=546),
    "boot_status": stbt.Region(160, 524, right=426, bottom=562),
    "bootloader_osd_display": stbt.Region(791, 455, right=914, bottom=485),
    "set_hide_loader_info_mode": stbt.Region(793, 198, right=916, bottom=228),
    "set_bootcheck_mode": stbt.Region(793, 144, right=916, bottom=174),
    "LOADER_DATA": stbt.Region(504, 134, right=780, bottom=180),
    "menu": stbt.Region(547, 31, right=596, bottom=57),
    "0x80000D06": stbt.Region(557, 576, right=707, bottom=602),
    "0x80000D06-": stbt.Region(557, 576, right=707, bottom=602),
    "0x80000D20": stbt.Region(557, 576, right=707, bottom=602),
    "0x80000D20-": stbt.Region(557, 576, right=707, bottom=602),
    "0x80000D21": stbt.Region(557, 576, right=707, bottom=602),
    "0x80000D07": stbt.Region(557, 576, right=707, bottom=602),
    "0x80000D07-": stbt.Region(557, 576, right=707, bottom=602),
    "0x80000D0D": stbt.Region(557, 576, right=707, bottom=602),
    "0x80000D0D-": stbt.Region(557, 576, right=707, bottom=602),
    "0x80000C0A": stbt.Region(557, 576, right=707, bottom=602),
    "0x80000C0A-": stbt.Region(557, 576, right=707, bottom=602),
    "0x80030031": stbt.Region(557, 576, right=707, bottom=602),
    "0x80030038": stbt.Region(557, 576, right=707, bottom=602),
    "0x80030003": stbt.Region(557, 576, right=707, bottom=602),
    "0x80001300": stbt.Region(557, 576, right=707, bottom=602),
    "err_code": stbt.Region(557, 576, right=707, bottom=602),
    "100%": stbt.Region(594, 408, right=677, bottom=458),
    "75%": stbt.Region(594, 408, right=677, bottom=458),
    "70%": stbt.Region(594, 408, right=677, bottom=458),
    "programming_flash": stbt.Region(621, 529, right=873, bottom=556),
    "download_usb": stbt.Region(663, 491, right=846, bottom=512),
    "usb_upgrade": stbt.Region(592, 278, right=734, bottom=317),
    "upgrade": stbt.Region(799, 525, right=894, bottom=550),
    "forced": stbt.Region(799, 525, right=894, bottom=550),
    "ok": stbt.Region(588, 522, right=654, bottom=554),
    "comecar": stbt.Region(547, 515, right=698, bottom=560),
    "start": stbt.Region(572, 522, right=675, bottom=553),
    "balxando_dados": stbt.Region(637, 530, right=850, bottom=550),
    "analyzing_upgrade_file": stbt.Region(521, 550, right=747, bottom=571),
    "downloading_data": stbt.Region(628, 530, right=867, bottom=556),
    # "fec": stbt.Region(803, 381, right=895, bottom=409),
    # "fec": stbt.Region(798, 393, right=887, bottom=419),
    "fec": stbt.Region(818, 202, right=880, bottom=231),
    "status": stbt.Region(268, 553, right=469, bottom=589),
    "config": stbt.Region(42, 54, right=350, bottom=100),
    "loader_menu": stbt.Region(96, 42, right=485, bottom=78),
    # "run_loader": stbt.Region(207, 541, right=450, bottom=578),
    "run_loader": stbt.Region(554, 545, right=734, bottom=590),
    # "loader_osd_output": stbt.Region(800, 181, right=901, bottom=218)
    # "loader_osd_output": stbt.Region(817, 194, right=881, bottom=206)
    "loader_osd_output": stbt.Region(800, 180, right=900, bottom=215),
    "serial_number": stbt.Region(335, 523, right=716, bottom=555),
    # "12345678": stbt.Region(800, 292, right=930, bottom=325),
    "12345678": stbt.Region(1065, 113, right=1170, bottom=147),
    "av_output_result": stbt.Region(329, 509, right=789, bottom=550),
    "manufacture_code": stbt.Region(357, 182, right=558, bottom=224),
    "manufacture_name": stbt.Region(355, 229, right=554, bottom=271),
    "model": stbt.Region(476, 279, right=559, bottom=321),
    "hw_version": stbt.Region(418, 328, right=559, bottom=373),
    "app_version": stbt.Region(412, 381, right=555, bottom=423),
    "loader_version": stbt.Region(385, 427, right=557, bottom=471),
    "boot_logo_version": stbt.Region(351, 481, right=557, bottom=518),
    "loader_res_version": stbt.Region(343, 530, right=554, bottom=571),
    "0.00": stbt.Region(230, 210, right=333, bottom=256),
    "russian_err_message": stbt.Region(426, 603, right=857, bottom=638),
    "spanish_err_message": stbt.Region(1026, 43, right=1176, bottom=72),
    "language_flag": stbt.Region(794, 396, right=911, bottom=425),
    "set_language_flag": stbt.Region(326, 506, right=702, bottom=548),
    "dsn_version": stbt.Region(608, 115, right=687, bottom=145),
    "module_versions": stbt.Region(794, 339, right=902, bottom=379),
    "loader_dsn": stbt.Region(416, 189, right=603, bottom=249),
    "loader_man_code": stbt.Region(416, 249, right=603, bottom=308),
    "loader_model_code": stbt.Region(416, 308, right=603, bottom=368),
    "loader_hw_ver": stbt.Region(416, 368, right=603, bottom=427),
    "loader_loader_ver": stbt.Region(416, 427, right=603, bottom=487),
    "loader_key_ver": stbt.Region(416, 487, right=603, bottom=546),
    "bandwidth": stbt.Region(784, 246, right=854, bottom=282),
    "tp_search": stbt.Region(137, 33, right=255, bottom=64),
    "signal_search": stbt.Region(81, 33, right=310, bottom=67),
    "strength": stbt.Region(876, 524, right=929, bottom=559),
    "quality": stbt.Region(877, 580, right=927, bottom=619),
    # "lock_state": stbt.Region(62, 92, right=169, bottom=125),
    "lock_state": stbt.Region(1109, 517, right=1147, bottom=562),
}

# the ocr mode to match text
ocr_modes = {

    "default": stbt.OcrMode.PAGE_SEGMENTATION_WITHOUT_OSD,
    "word": stbt.OcrMode.SINGLE_WORD,
    "line": stbt.OcrMode.SINGLE_LINE,
    "character": stbt.OcrMode.SINGLE_CHARACTER
}

# package info to be used in  match a particular text, format:[(text,region,ocr_mode),(....)]
ocr_info = {

    # "menu": [(texts["menu"], None, None)],
    "menu": [(texts["menu"], regions["menu"], ocr_modes["line"])],
    # "0x80000D06": [(texts["0x80000D06"], regions["0x80000D06"], ocr_modes["line"])],
    "0x80000D06": [(texts["0x80000D06"], regions["0x80000D06"], None)],
    "0x80000D06-": [(texts["0x80000D06-"], regions["0x80000D06-"], None)],
    "0x80000D20": [(texts["0x80000D20"], regions["0x80000D20"], None)],
    "0x80000D20-": [(texts["0x80000D20-"], regions["0x80000D20-"], None)],
    "0x80000D21": [(texts["0x80000D21"], regions["0x80000D21"], None)],
    "0x80000D07": [(texts["0x80000D07"], regions["0x80000D07"], None)],
    "0x80000D07-": [(texts["0x80000D07-"], regions["0x80000D07-"], None)],
    "0x80000D0D": [(texts["0x80000D0D"], regions["0x80000D0D"], None)],
    "0x80000D0D-": [(texts["0x80000D0D-"], regions["0x80000D0D-"], None)],
    "0x80000D0D--": [(texts["0x80000D0D--"], regions["0x80000D0D-"], None)],
    "0x80000C0A": [(texts["0x80000C0A"], regions["0x80000C0A"], None)],
    "0x80000C0A-": [(texts["0x80000C0A-"], regions["0x80000C0A-"], None)],
    "0x80000C0A--": [(texts["0x80000C0A--"], regions["0x80000C0A-"], None)],
    "0x80000C0A---": [(texts["0x80000C0A---"], regions["0x80000C0A-"], None)],
    "0x80030003": [(texts["0x80030003"], regions["0x80030003"], None)],
    "0x80030031": [(texts["0x80030031"], regions["0x80030031"], None)],
    "0x80001300": [(texts["0x80001300"], regions["0x80001300"], None)],
    "0x80001300-": [(texts["0x80001300-"], regions["0x80001300"], None)],
    "0x80000D02": [(texts["0x80000D02"], regions["err_code"], None)],
    "0x80000D30": [(texts["0x80000D30"], regions["err_code"], None)],
    "0x80000D41": [(texts["0x80000D41"], regions["err_code"], None)],
    "loader_err_code": [(texts["loader_err_code"], regions["err_code"], None)],
    "0x80030038": [(texts["0x80030038"], None, None)],
    "100%": [(texts["100%"], regions["100%"], None)],
    "75%": [(texts["75%"], regions["75%"], None)],
    "70%": [(texts["70%"], regions["70%"], None)],
    "1.20": [(texts["1.20"], regions["1.20"], None)],
    "20000": [(texts["20000"], regions["20000"], None)],
    "download_usb": [(texts["download_usb"], regions["download_usb"], None)],
    "salvando": [(texts["salvando"], None, None)],
    "plase_choose": [(texts["plase_choose"], None, None)],
    "programming_flash": [(texts["programming_flash"], None, None)],
    "analyzing_upgrade_file": [(texts["analyzing_upgrade_file"], regions["analyzing_upgrade_file"], ocr_modes["line"])],
    # "analyzing_upgrade_file": [(texts["analyzing_upgrade_file"], None, None)],
    # "downloading_data": [(texts["downloading_data"], regions["downloading_data"], ocr_modes["line"])],
    "downloading_data": [(texts["downloading_data"], None, None)],
    "upgrade": [(texts["upgrade"], regions["upgrade"], ocr_modes["line"])],
    "forced": [(texts["forced"], regions["forced"], ocr_modes["line"])],
    "ok": [(texts["ok"], regions["ok"], ocr_modes["line"])],
    "comecar": [(texts["comecar"], regions["comecar"], ocr_modes["line"])],
    "start": [(texts["start"], regions["start"], ocr_modes["line"])],
    "balxando_dados": [(texts["balxando_dados"], None, None)],
    "usb_upgrade": [(texts["usb_upgrade"], regions["usb_upgrade"], ocr_modes["line"])],
    "error_0x0": [("ERROR: 0x0", regions["error_code"], ocr_modes["line"]),
                  ("Download completed successfully!", regions["error_info"], ocr_modes["line"])],

    "error_0x13": [("ERROR: 0x13", regions["error_code"], ocr_modes["line"]),
                   ("The module verslon ls Incorrect.", regions["error_info"], ocr_modes["line"])],

    "error_0x14": [("ERROR: 0x14", regions["error_code"], ocr_modes["line"]),
                   ("The module verslon ls same as STB's.", regions["error_info"], ocr_modes["line"])],

    "error_0xc2": [("ERROR:", regions["error_code"], ocr_modes["line"]),
                   ("download be found", regions["error_info"], ocr_modes["line"])],

    "error_0x21": [("ERROR: 0x21", regions["error_code"], ocr_modes["line"]),
                   ("Resident key content error.", regions["error_info"], ocr_modes["line"])],

    "error_0x27": [("ERROR: 0x27", regions["error_code"], ocr_modes["line"]),
                   ("The length of the", regions["error_info"], ocr_modes["line"])],

    "error_0x26": [("ERROR: 0x26", regions["error_code"], ocr_modes["line"]),
                   ("Slgnature verlflcatlon has falled.", regions["error_info"], ocr_modes["line"])],

    "error_0x40": [("ERROR: 0x40", regions["error_code"], ocr_modes["line"]),
                   ("System ID does not match that of STB.", regions["error_info"], ocr_modes["line"])],

    "error_0x51": [("ERROR: 0x51", regions["error_code"], ocr_modes["line"]),
                   ("The data Id of the header does not equal 0x11.", regions["error_info"], ocr_modes["line"])],

    "error_0x54": [("ERROR: 0x54", regions["error_code"], ocr_modes["line"]),
                   ("manufacturer Id does not match that of STB.", regions["error_info"], ocr_modes["line"])],

    "error_0x55": [("ERROR: 0x55", regions["error_code"], ocr_modes["line"]),
                   ("hardware version does not match that of STB.", regions["error_info"], ocr_modes["line"])],

    # download sequence number does not match that of STB.
    "error_0x56": [("ERROR: 0x56", regions["error_code"], ocr_modes["line"]),
                   ("download sequence number does not match", regions["error_info"], ocr_modes["line"])],

    # download sequence number Is ldentlcal to that of STB.
    "error_0x57": [("ERROR: 0x57", regions["error_code"], ocr_modes["line"]),
                   ("download sequence number Is", regions["error_info"], ocr_modes["line"])],

    "error_0x65": [("ERROR: 0x65", regions["error_code"], ocr_modes["line"]),
                   ("The varlant does not match that of STB.", regions["error_info"], ocr_modes["line"])],

    "error_0x66": [("ERROR: 0x66", regions["error_code"], ocr_modes["line"]),
                   ("The sub-variant does not match that of STB.", regions["error_info"], ocr_modes["line"])],

    "error_0x82": [("ERROR: 0x82", regions["error_code"], ocr_modes["line"])],

    "error_0x83": [("ERROR: 0x83", regions["error_code"], ocr_modes["line"]),
                   ("Acqulre a download sectlon timeout.", regions["error_info"], ocr_modes["line"])],

    "error_0xff": [("ERROR: 0xff", regions["error_code"], ocr_modes["line"]),
                   ("Tune transport stream falled.", regions["error_info"], ocr_modes["line"])],

    "download_DDB": [(texts["download_DDB"], regions["download_process"], ocr_modes["line"])],

    "loading_data": [(texts["loading_data"], regions["download_process"], ocr_modes["line"])],

    "process_m1": [(texts["process_m1"], regions["download_process"], ocr_modes["line"])],

    "process_m2": [(texts["process_m2"], regions["download_process"], ocr_modes["line"])],

    "process_m3": [(texts["process_m3"], regions["download_process"], ocr_modes["line"])],

    "boot_status": [("Start high level code...", regions["boot_status"], ocr_modes["line"])],

    "Flash_test": [("Flash test", regions["boot_status"], ocr_modes["line"])],

    "LOADER READY": [("LOADER READY", regions["download_process"], ocr_modes["line"])],

    "status": [(texts["status"], regions["status"], ocr_modes["line"])],

    "config": [(texts["config"], regions["config"], ocr_modes["line"])],

    "loader_menu": [(texts["loader_menu"], regions["loader_menu"], ocr_modes["line"])],

    "run_loader": [(texts["run_loader"], regions["run_loader"], ocr_modes["line"])],

    "run_app": [(texts["run_app"], regions["run_loader"], ocr_modes["line"])],

    "serial_number": [(texts["serial_number"], regions["serial_number"], ocr_modes["line"])],

    "12345678": [(texts["12345678"], regions["12345678"], ocr_modes["line"])],

    "av_output_result": [(texts["av_output_result"], regions["av_output_result"], ocr_modes["line"])],

    "manufacture_code": [(texts["manufacture_code"], regions["manufacture_code"], ocr_modes["line"])],

    "manufacture_name": [(texts["manufacture_name"], regions["manufacture_name"], ocr_modes["line"])],

    "model": [(texts["model"], regions["model"], ocr_modes["line"])],

    "hw_version": [(texts["hw_version"], regions["hw_version"], ocr_modes["line"])],

    "app_version": [(texts["app_version"], regions["app_version"], ocr_modes["line"])],

    "loader_version": [(texts["loader_version"], regions["loader_version"], ocr_modes["line"])],

    "boot_logo_version": [(texts["boot_logo_version"], regions["boot_logo_version"], ocr_modes["line"])],

    "loader_res_version": [(texts["loader_res_version"], regions["loader_res_version"], ocr_modes["line"])],

    "russian_err_message": [(texts["russian_err_message"], regions["russian_err_message"], ocr_modes["line"])],

    "spanish_err_message": [(texts["spanish_err_message"], regions["spanish_err_message"], ocr_modes["line"])],

    "set_language_flag": [(texts["set_language_flag"], regions["set_language_flag"], ocr_modes["line"])],

    "dsn_version_1001": [(texts["dsn_version_1001"], regions["dsn_version"], ocr_modes["line"])],

    "dsn_version_1000": [(texts["dsn_version_1000"], regions["dsn_version"], ocr_modes["line"])],

    "dsn_version_1100": [(texts["dsn_version_1100"], regions["dsn_version"], ocr_modes["line"])],

    "dsn_version_1101": [(texts["dsn_version_1101"], regions["dsn_version"], ocr_modes["line"])],

    "dsn_version_1102": [(texts["dsn_version_1102"], regions["dsn_version"], ocr_modes["line"])],

    "dsn_version_1103": [(texts["dsn_version_1103"], regions["dsn_version"], ocr_modes["line"])],

    "dsn_version_1104": [(texts["dsn_version_1104"], regions["dsn_version"], ocr_modes["line"])],

    "module_version_1001": [(texts["module_version_1001"], regions["module_versions"], ocr_modes["line"])],

    "module_version_1000": [(texts["module_version_1000"], regions["module_versions"], ocr_modes["line"])],

    "module_version_1100": [(texts["module_version_1100"], regions["module_versions"], ocr_modes["line"])],

    "module_version_1101": [(texts["module_version_1101"], regions["module_versions"], ocr_modes["line"])],

    "module_version_1102": [(texts["module_version_1102"], regions["module_versions"], ocr_modes["line"])],

    "module_version_1103": [(texts["module_version_1103"], regions["module_versions"], ocr_modes["line"])],

    "module_version_1104": [(texts["module_version_1104"], regions["module_versions"], ocr_modes["line"])],

    "loader_dsn": [(texts["loader_dsn"], regions["loader_dsn"], ocr_modes["line"])],

    "loader_man_code": [(texts["loader_man_code"], regions["loader_man_code"], ocr_modes["line"])],

    "loader_model_code": [(texts["loader_model_code"], regions["loader_model_code"], ocr_modes["line"])],

    "loader_hw_ver": [(texts["loader_hw_ver"], regions["loader_hw_ver"], ocr_modes["line"])],

    "loader_loader_ver": [(texts["loader_loader_ver"], regions["loader_loader_ver"], ocr_modes["line"])],

    "loader_key_ver": [(texts["loader_key_ver"], regions["loader_key_ver"], ocr_modes["line"])],

}


def test_accurate_ocr():
    """
    internal function to extract texts from HDMI output
    :return: None
    """
    # result = stbt.ocr(region=regions['dsn'], mode=ocr_modes['word'],tesseract_user_patterns=u'\n')
    # print result
    result = stbt.ocr(region=regions["LOADER_DATA"], mode=ocr_modes['line'], tesseract_user_patterns=[u'\n', u'\p'])

    print type(result)
    print result
    # assert result == u"ISIGN Ver: *"
    # result = stbt.ocr(region=regions['dsn'], mode=ocr_modes['line'], tesseract_user_patterns=u'\n')
    # print result
    # result = stbt.ocr(region=regions['dsn_region'], mode=ocr_modes['line'], tesseract_user_patterns=u'\n')
    # print result
    # result = stbt.ocr(region=regions['dsn_region'], mode=ocr_modes['word'], tesseract_user_patterns=u'\n')

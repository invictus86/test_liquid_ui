"""
This module defined some customized Error types.
author: loren.huang@ekt-digital.com
date: 2018-10-15
"""


class TimeoutError(BaseException):

    def __init__(self):
        err = "connect to redrathub timed out ,make sure the redrathub service is on"
        super(TimeoutError, self).__init__(err)

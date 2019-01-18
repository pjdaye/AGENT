#!/usr/bin/env python

import logging
import sys
from datetime import datetime

LOG_SILENT = 0x00
LOG_ISSUE = 0x01
LOG_ERROR = 0x02
LOG_METHODS = 0x04
LOG_INFO = 0x08
LOG_TRACE = 0x10

INFO_FMT = "[INFO] => [{} - {}] [MESSAGE: {}]"
ERROR_FMT = "[ERROR] => [{} - {} ] [MESSAGE: {}]"
ISSUE_FMT = "[ISSUE:{}] [CONTEXT_ID: {}] [TRACE-INFO: {} - {} ] [MESSAGE: {}]"
TRACE_FMT = "[TRACE:{}] [CONTEXT_ID: {}] [TRACE-INFO: {} - {} ] [MESSAGE: {}]"


class Logger:
    def __init__(self):
        self.__level = LOG_INFO | LOG_ERROR | LOG_METHODS
        self.depth = 99
        self.__logger = logging.getLogger("TestAgent")
        self.__logger.setLevel(logging.DEBUG)
        if len(self.__logger.handlers) < 1:
            formatter = logging.Formatter('%(message)s')
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            self.__logger.addHandler(ch)

    def SetLogLevel(self, new_log_level):
        self.__level = new_log_level

    def GetLogLevel(self):
        return self.__level

    def Start(self, context, class_name, method_name, params):
        if self.__level & LOG_METHODS:
            self.__formatted_log(START_FMT, context, class_name, method_name, str(params))

    def End(self, context, class_name, method_name):
        if self.__level & LOG_METHODS:
            self.__formatted_log(END_FMT, context, class_name, method_name, "")

    def Info(self, context, class_name, method_name, message):
        if self.__level & LOG_INFO:
            message.replace('\r', '\\r').replace('\n', '\\n')
            self.__formatted_log(INFO_FMT, context, class_name, method_name, message)

    def Issue(self, context, class_name, method_name, message):
        if self.__level & LOG_ISSUE:
            message.replace('\r', '\\r').replace('\n', '\\n')
            self.__formatted_log(ISSUE_FMT, context, class_name, method_name, message)

    def Trace(self, context, class_name, method_name, message, depth=0):
        if self.__level & LOG_TRACE and depth <= self.depth:
            message += " depth:{}".format(depth)
            self.__formatted_log(TRACE_FMT, context, class_name, method_name, message)

    def Error(self, context, class_name, method_name, message):
        if self.__level & LOG_ERROR:
            message.replace('\r', '\\r').replace('\n', '\\n')
            self.__formatted_log(ERROR_FMT, context, class_name, method_name, message)

    def __formatted_log(self, fmt_string, context, class_name, method_name, message):
        if not context is None:
            context_id = context.id
        else:
            context_id = "No context provided"
        timestamp = datetime.now()
        # msg = fmt_string.format(timestamp, context_id, class_name, method_name, message)
        msg = fmt_string.format(class_name, method_name, message)
        self.__log(msg)

    def __log(self, msg):
        '''
           Writing to stderr.  Alternative would be to set 	WSGIRestrictStdout Off  in the httpd.conf file for each python service
        :param msg:
        :return:
        '''
        #sys.stderr.write(msg + " \n")
        #sys.stderr.flush()
        self.__logger.debug(msg)


    def Report(self, msg):
        if self.__level & LOG_ISSUE:
            sys.stdout.write("REPORT: {0} \n".format(msg))

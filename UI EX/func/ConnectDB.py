# -*- coding:utf-8 -*-
from func.ConnectDBFA import connectDBFA
from func.ConnectDBSMT import connectDBSMT
from func.ConnectDBPlugin import connectDBPlugin


class ConnectDB(connectDBFA, connectDBSMT, connectDBPlugin):
    pass

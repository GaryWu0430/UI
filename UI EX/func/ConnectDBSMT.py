# -*- coding:utf-8 -*-
from func.sqlf.SQLHelper import SqlHelperSMT


class connectDBSMT():

    def CheckRoutingSMT(self, SN, station_name):
        if SN == "ZZ99999":
            return ("PASS", "This SN data won't update to shopfloor", "")
        else:
            iResult = ""
            iMessage = ""
            host = "10.226.32.101"
            user = "execuser"
            password = "exec7*user"
            database = "SMT"
            sqlHelper = SqlHelperSMT(host, user, password, database)
            result = sqlHelper.CheckStatusSMT(SN, station_name)
            iParamAll = ""
            if ("iResult") in result:
                iResult = str(result["iResult"]).strip()
                iMessage = str(result["iMessage"]).strip()
                if iResult.upper() == "PASS":
                    iParamAll = ""
            return (iResult, iMessage, iParamAll)

    def UpdateToSMTDB(self, SN, station_name, result, inputstring, line=""):
        iResult = "FAIL"
        iMessage = "Update Fail"
        if SN == "ZZ99999":
            return ("PASS", "ShopFloor System Disabled")
        else:
            host = "10.226.32.101"
            user = "execuser"
            password = "exec7*user"
            database = "SMT"
            sqlHelper = SqlHelperSMT(host, user, password, database)
            inputstring = "SN=%s##" % (SN) + inputstring
            result = sqlHelper.UpdateSFSMT(SN, station_name, result, inputstring, line)
            print("inputstring={}".format(inputstring))
            print("result={}".format(result))
            if "iResult" in result:
                iResult = str(result["iResult"]).strip()
                iMessage = str(result["iMessage"]).strip()
            return (iResult, iMessage)

    def macSMT(self, SN):
        if SN == "ZZ99999":
            return ("PASS", u"此SN的测试数据将不更新到数据库中", "")
        else:
            host = "10.226.32.101"
            user = "execuser"
            password = "exec7*user"
            database = "SMT"
            sqlHelper = SqlHelperSMT(host, user, password, database)
            result = sqlHelper.getMAC(SN)
            print(result)
            return result

    def IMEISMT(self, SN):
        if SN == "ZZ99999":
            return ("PASS", u"此SN的测试数据将不更新到数据库中", "")
        else:
            host = "10.226.32.101"
            user = "execuser"
            password = "exec7*user"
            database = "SMT"
            sqlHelper = SqlHelperSMT(host, user, password, database)
            result = sqlHelper.getIMEI(SN)
            print(result)
            return result[0][1]

    def SMTHWinfo(self, SN):
        if SN == "ZZ99999":
            return ("PASS", u"此SN的测试数据将不更新到数据库中", "")
        else:
            host = "10.226.32.101"
            user = "execuser"
            password = "exec7*user"
            database = "SMT"
            sqlHelper = SqlHelperSMT(host, user, password, database)
            result = sqlHelper.getHWinfo(SN)
            print(result)
            return result[0][1]

    def SMTPN(self, SN):
        if SN == "ZZ99999":
            return ("PASS", u"此SN的测试数据将不更新到数据库中", "")
        else:
            host = "10.226.32.101"
            user = "execuser"
            password = "exec7*user"
            database = "SMT"
            sqlHelper = SqlHelperSMT(host, user, password, database)
            result = sqlHelper.getPN(SN)
            print(result)
            return result

    def UpdateMAC(self, SN, MAC, mactype):
        if SN == "ZZ99999":
            return ("PASS", u"此SN的测试数据将不更新到数据库中", "")
        else:
            host = "10.226.32.101"
            user = "execuser"
            password = "exec7*user"
            database = "SMT"
            sqlHelper = SqlHelperSMT(host, user, password, database)
            result = sqlHelper.UpdateMAC(SN, MAC, mactype)
            print(result)
            return result

    def RecordtoSF(self, SN, funName, funValue):
        if SN == "ZZ99999":
            return ("PASS", u"此SN的测试数据将不更新到数据库中", "")
        else:
            host = "10.226.32.101"
            user = "execuser"
            password = "exec7*user"
            database = "SMT"
            sqlHelper = SqlHelperSMT(host, user, password, database)
            result = sqlHelper.RecordtoSF(SN, funName, funValue)

            result = result['@OutPutStr']
            print("result:", type(result))
            print("-----------------------")
            return result

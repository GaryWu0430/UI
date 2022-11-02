# -*- coding:utf-8 -*-
from func.sqlf.SQLHelper import SqlHelperFA


class connectDBFA():

    def CheckRoutingFA(self, SN, station_name, OPID, fixture_sn):
        if SN == "ZZ99999":
            return ("PASS", u"此SN的测试数据将不更新到数据库中", "")

        else:
            host = "10.226.32.111"
            user = "SDT"
            password = "SDT#7"
            database = "CAR"
            sqlHelper = SqlHelperFA(host, user, password, database)
            # fixture_sn的内容是一个列表，把它转换成字符串
            if fixture_sn is not None:
                FixtureX = 'FixtureX=' + '##FixtureX='.join(fixture_sn)
                inputstring = "SN=%s;$;OPID=%s;$;%s" % (SN, OPID, FixtureX)
            else:
                inputstring = "SN=%s;$;OPID=%s;$;" % (SN, OPID)
            print(inputstring)
            result = sqlHelper.CheckStatusFA(SN, station_name)
            iParamAll = ""
            if "iResult" in result:
                iResult = result["iResult"].strip()
                iMessage = result["iMessage"].strip()
                if result["iResult"].strip().upper() == "PASS":
                    iParamAll = result["iParamAll"]

            return (iResult, iMessage, iParamAll)

    def UpdateToFADB(self, SN, station_name, result, inputstring):
        if SN == "ZZ99999":
            return ("PASS", "ShopFloor System Disabled")

        else:
            host = "10.226.32.111"
            # host = 'CA2051841\\SQLEXPRESS'
            # host = "172.26.6.66"
            user = "SDT"
            password = "SDT#7"
            database = "CAR"
            sqlHelper = SqlHelperFA(host, user, password, database)

            inputstring = "SN=%s##" % (SN) + inputstring

            result = sqlHelper.UpdateSFFA(SN, station_name, result, inputstring)
            if "iResult" in result:
                iResult = result["iResult"].strip()
                iMessage = result["iMessage"].strip()

            return (iResult, iMessage)

    def AT_LinkCompSN(self, SN, station_name, data):
        host = "10.226.32.111"
        user = "SDT"
        password = "SDT#7"
        database = "SEL"
        sqlHelper = SqlHelperFA(host, user, password, database)

        bu = "SEL"
        step = "AT_LinkCompSN"

        inputstring = "SN=%s;$;%s" % (SN, data)

        result = sqlHelper.MonitorPortal(bu, station_name, step, inputstring)

        try:
            if "@OutPutStr" in result:
                return result["@OutPutStr"].strip()
            else:
                return result[""].strip()
        except BaseException:
            return u"Link失败，请联系SE"

    def ParseKeyValuePairs(self, raw_data):
        host = "10.226.32.111"
        user = "SDT"
        password = "SDT#7"
        database = "SEL"
        sqlHelper = SqlHelperFA(host, user, password, database)
        result = sqlHelper.ParseKeyValuePairs(raw_data, True, True)
        return result

    def SFCompareFA( self, sn, value, key, station, line) :
        if sn == "ZZ99999" :
            return ( "PASS", u"此SN的测试数据将不更新到数据库中", "" )
        else :
            host = "10.226.32.111"
            user = "SDT"
            password = "SDT#7"
            database = "CAR"
            sqlHelper = SqlHelperFA( host, user, password, database )
            result = sqlHelper.SP_Diagnose_Compare(sn,value,key,station, line)
            return result

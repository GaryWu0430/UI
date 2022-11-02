# -*- coding:utf-8 -*-
import time
import pymssql
import re

"""
information :

1. PLZ add the item that you need in `getinfo` function manually.

Functions:

checkRoutingSMT() -- check routing in SMT.              Return (iResult, iMessage, iParamAll)
checkRoutingFA()  -- check routing in FA.               Return (iResult, iMessage, iParamAll)
UpdateSMT()       -- update status in SMT.              Return (iResult, iMessage, iParamAll)
UpdateFA()        -- update status in FA.               Return (iResult, iMessage, iParamAll)
getinfo()         -- get SN information with item name. Return LIST[(item_name, item_value)]

"""


class connectDBPlugin():

    def __init__(self):
        self.host = None
        self.user = None
        self.password = None
        self.database = None
        self.sql = None
        self.conn = None

    def checkRoutingSMT(self, sn, station):
        ret = {}
        self.__getSqlInfo("SMT", "CHECKROUTING")
        try:
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
        except Exception as e:
            time.sleep(0.1)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return self.__formatData(ret)
        sql = self.sql.format(func='SP_RoutingCheck', sn=sn, station=station)
        ret = self.__execute(sql)
        self.conn.commit()
        self.conn.close()
        return self.__formatData(ret)

    def checkRoutingFA(self, sn, station):
        ret = {}
        self.__getSqlInfo("FA", "CHECKROUTING")
        try:
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
        except Exception as e:
            time.sleep(0.1)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return self.__formatData(ret)
        sql = self.sql.format(func='SP_Diagnose_CheckMEStatus', sn=sn, station=station)
        print(sql)
        ret = self.__execute(sql)
        self.conn.commit()
        self.conn.close()
        return self.__formatData(ret)

    def UpdateSMT(self, sn, line, station, result, fixtureID, inputstring):
        ret = {}
        self.__getSqlInfo("SMT", "UPDATE")
        try:
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
        except Exception as e:
            time.sleep(0.1)
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return self.__formatData(ret)
        sql = self.sql.format(func='usp_TestResultSave', sn=sn, line=line, station=station, result=result, fixtureID=fixtureID, inputstring=inputstring)
        ret = self.__execute(sql)
        self.conn.commit()
        self.conn.close()
        return self.__formatData(ret)

    def UpdateFA(self, sn, station, result, inputstring):
        ret = {}
        self.__getSqlInfo("FA", "UPDATE")
        try:
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
        except Exception as e:
            time.sleep(0.1)
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return self.__formatData(ret)
        sql = self.sql.format(func='SP_Diagnose_SaveResultNew', sn=sn, station=station, result=result, inputstring=inputstring)
        ret = self.__execute(sql)
        self.conn.commit()
        self.conn.close()
        return self.__formatData(ret)

    def getinfo(self, sn, item):
        ret = {}
        if item not in ["HWINFO", "IMEI", "MAC", "CPUID", "PN"]:
            return
        self.__getSqlInfo("SMT", "GETINFO")
        try:
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, charset="utf8", login_timeout=30)
        except Exception as e:
            time.sleep(0.1)
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return self.__formatData(ret)
        sql = self.sql.format(item=item, sn=sn)
        cur = self.conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        if "0" == ret[0][0]:
            return
        return ret

    def __getSqlInfo(self, area, action):
        # SMT DB information
        if "SMT" in area.upper():
            self.host = "10.226.32.101"
            self.user = "execuser"
            self.password = "exec7*user"
            self.database = "SMT"
            if "CHECK" in action.upper():
                self.sql = r"DECLARE @ReturnValue varchar(2000)  EXEC {func} '{sn}','{station}','',''  SELECT @ReturnValue "
            elif "UPDATE" in action.upper():
                self.sql = r"Declare @ReturnValue VARCHAR(3000) Declare @iResult VARCHAR(1) Declare @iMessage VARCHAR(100) EXEC {func} @SN='{sn}',@LINE='{line}',@station='{station}', @TestResult='{result}', @Path ='' ,@FileName='', @FixtureID='{fixtureID}',@OperatorID='', @Result =@iResult OUTPUT,@msg=@iMessage OUTPUT ,@PortID='',@InPutStr=N'{inputstring}'; SELECT  @iResult as N'iResult',@iMessage as N'iMessage'"
            elif "GETINFO" in action.upper():
                self.sql = r"DECLARE @p1 varchar(1000) SET @p1 = '' DECLARE @p2 varchar(1000) SET @p2 = '' EXEC usp_GetDataFromSMT @Type = '{item}',@SN='{sn}',@Result = @p1 output,@msg = @p2 output SELECT  @p1 as Result, @p2 as Msg"

        # FA DB information
        elif "FA" in area.upper():
            self.host = "10.226.32.111"
            self.user = "SDT"
            self.password = "SDT#7"
            self.database = "CAR"
            if "CHECK" in action.upper():
                self.sql = r"DECLARE @ReturnValue varchar(2000) EXEC {func} '{sn}','{station}','','' SELECT @ReturnValue"
            elif "UPDATE" in action.upper():
                self.sql = r"DECLARE @ReturnValue varchar(2000) EXEC {func} '{sn}','{station}','','{result}','{inputstring}','##','','','' SELECT @ReturnValue"

    def __ParseKeyValuePairs(self, iParamAll, remove_set_prefix=True, msdb=True):
        ret = {}
        sep = ';' if msdb else '\r\n'
        for line in filter(None, iParamAll.split(sep)):
            if remove_set_prefix:
                line = re.sub(r'(?i)^set ', '', line)
            key, equals, value = line.partition('=')
            if equals:
                if len(value.strip()) > 0:
                    ret[key] = value
        return ret

    def __execute(self, sql):
        ret = {}
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            index = cur.description
            result = []
            for res in cur.fetchall():
                row = {}
            for i in range(len(index)):
                row[index[i][0]] = res[i]
            result.append(row)
            cur.close()
            for res in result:
                for (k, v) in res.items():
                    ret[k] = v
        except Exception as e:
            time.sleep(0.1)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
        return ret

    def __formatData(self, result):
        iResult = ""
        iMessage = ""
        iParamAll = ""
        if "iResult" in result:
            iResult = str(result["iResult"]).strip()
            iMessage = str(result["iMessage"]).strip()
            if "iParamAll" in result and iResult.upper() == "PASS":
                iParamAll = result["iParamAll"]
        return (iResult.upper(), iMessage, iParamAll)

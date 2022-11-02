#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymssql
import time
import re
import logging
from func.sqlf.InterfaceSQL import interfaceSQL


class SqlHelperFA(interfaceSQL):

    def __init__(self, host, user, password, database):
        self.debug_mode = True
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def GetConnect(self):
        if not self.database:
            raise(NameError, "Please config database first!")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset="utf8", login_timeout=30)
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "Connect database fail!")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.GetConnect()
        cur.execute(sql)
        index = cur.description
        result = []
        for res in cur.fetchall():
            row = {}
        for i in range(len(index)):
            row[index[i][0]] = res[i]
        result.append(row)
        self.conn.close()
        return result

    def ExecNonQuery(self, sql):
        cur = self.GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def CheckStatusFA(self, sn, station):
        ret = {}
        if self.debug_mode:
            print("start")
        try:
            if self.debug_mode:
                print("Connect SF_DB")
            # print('_DB_SERVER:'+_DB_SERVER+'_DB_NAME:'+_DB_NAME+'_DB_USER:'+_DB_USER+'_DB_PSSWD:'+_DB_PSSWD)
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
            if self.debug_mode:
                print("DB Connected!!")
        except Exception as e:
            if self.debug_mode:
                print("SF_DB connect Exception:\n", e)
            time.sleep(0.1)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return ret
        if self.debug_mode:
            print("Post input string to DB SP")

        sql = '''
    DECLARE @ReturnValue varchar(2000)
    EXEC %s '%s','%s','%s','%s'
    SELECT @ReturnValue ''' % ('SP_Diagnose_CheckMEStatus', sn, station, "SN", "")  # SP_Diagnose_CheckMEStatus
        # print sql
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
            # outputstring = cur.fetchall()[0]
            cur.close()
            outputstring = result

            for res in result:
                if self.debug_mode:
                    print(res)
                    # print i
                    # i=i+1
                for (k, v) in res.items():
                    ret[k] = v
                    if self.debug_mode:
                        print("dict[{}] = {}".format(k, v))

            self.conn.commit()
            if self.debug_mode:
                print("SF_MSG = {}".format(outputstring))
        except Exception as e:
            if self.debug_mode:
                print("SF_DB Operate Exception: {}\n".format(e))
        self.conn.close()
        if self.debug_mode:
            print("SF DB Closed")
        return ret

    def CSNCheckStatusFA(self, sn, station):
        ret = {}
        if self.debug_mode:
            print("start")
        try:
            if self.debug_mode:
                print("Connect SF_DB")
            # print('_DB_SERVER:'+_DB_SERVER+'_DB_NAME:'+_DB_NAME+'_DB_USER:'+_DB_USER+'_DB_PSSWD:'+_DB_PSSWD)
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
            if self.debug_mode:
                print("DB Connected!!")
        except Exception as e:
            if self.debug_mode:
                print("SF_DB connect Exception:\n", e)
            time.sleep(0.1)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return ret
        if self.debug_mode:
            print("Post input string to DB SP")

        sql = '''
    DECLARE @ReturnValue varchar(2000)
    EXEC %s '%s','%s','%s','%s'
    SELECT @ReturnValue ''' % ('SP_Diagnose_CheckMEStatus', sn, station, "CSN", "")  # SP_Diagnose_CheckMEStatus
        # print sql
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
            # outputstring = cur.fetchall()[0]
            cur.close()
            outputstring = result

            for res in result:
                if self.debug_mode:
                    print(res)
                    # print i
                    # i=i+1
                for (k, v) in res.items():
                    ret[k] = v
                    if self.debug_mode:
                        print("dict[{}] = {}".format(k, v))

            self.conn.commit()
            if self.debug_mode:
                print("SF_MSG = {}".format(outputstring))
        except Exception as e:
            if self.debug_mode:
                print("SF_DB Operate Exception:\n", e)
        self.conn.close()
        if self.debug_mode:
            print("SF DB Closed")
        return ret

    def CheckOPIDFA(self, UserID, station):
        ret = {}
        if self.debug_mode:
            print("start")
        try:
            if self.debug_mode:
                print("Connect SF_DB")
            # print('_DB_SERVER:'+_DB_SERVER+'_DB_NAME:'+_DB_NAME+'_DB_USER:'+_DB_USER+'_DB_PSSWD:'+_DB_PSSWD)
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
            if self.debug_mode:
                print("DB Connected!!")
        except Exception as e:
            if self.debug_mode:
                print("SF_DB connect Exception:\n", e)
            time.sleep(0.1)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return ret
        if self.debug_mode:
            print("Post input string to DB SP")

        sql = '''
    DECLARE @ReturnValue varchar(2000)
    EXEC %s '%s','%s'
    SELECT @ReturnValue ''' % ('usp_ChkOPID', UserID, station)
        # print sql
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
            # outputstring = cur.fetchall()[0]
            cur.close()
            outputstring = result

            for res in result:
                if self.debug_mode:
                    print(res)
                    # print i
                    # i=i+1
                for (k, v) in res.items():
                    ret[k] = v
                    if self.debug_mode:
                        print("dict[{}] = {}".format(k, v))

            self.conn.commit()
            if self.debug_mode:
                print("SF_MSG = {}".format(outputstring))
        except Exception as e:
            if self.debug_mode:
                print("SF_DB Operate Exception:\n", e)
        self.conn.close()
        if self.debug_mode:
            print("SF DB Closed")
        return ret

    def CheckFixtureID(self, modelname, station, inputstring):
        ret = {}
        if self.debug_mode:
            print("start")
        try:
            if self.debug_mode:
                print("Connect SF_DB")
            # print('_DB_SERVER:'+_DB_SERVER+'_DB_NAME:'+_DB_NAME+'_DB_USER:'+_DB_USER+'_DB_PSSWD:'+_DB_PSSWD)
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
            if self.debug_mode:
                print("DB Connected!!")
        except Exception as e:
            if self.debug_mode:
                print("SF_DB connect Exception:\n", e)
            time.sleep(0.1)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return ret
        if self.debug_mode:
            print("Post input string to DB SP")

        sql = '''
    DECLARE @ReturnValue varchar(2000)
    EXEC %s '%s','%s','%s','%s','%s','%s'
    SELECT @ReturnValue ''' % ('SP_Diagnose_Check', '', modelname, station, "P21", inputstring, ';$;')
        # print sql
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
            # outputstring = cur.fetchall()[0]
            cur.close()
            outputstring = result

            for res in result:
                if self.debug_mode:
                    print(res)
                    # print i
                    # i=i+1
                for (k, v) in res.items():
                    ret[k] = v
                    if self.debug_mode:
                        print("dict[{}] = {}".format(k, v))

            self.conn.commit()
            if self.debug_mode:
                print("SF_MSG = {}".format(outputstring))
        except Exception as e:
            if self.debug_mode:
                print("SF_DB Operate Exception:\n", e)
        self.conn.close()
        if self.debug_mode:
            print("SF DB Closed")
        return ret

    def UpdateSFFA(self, sn, station, result, inputstring):
        ret = {}
        if self.debug_mode:
            print("start")
        try:
            if self.debug_mode:
                print("Connect SF_DB")
            # print('_DB_SERVER:'+_DB_SERVER+'_DB_NAME:'+_DB_NAME+'_DB_USER:'+_DB_USER+'_DB_PSSWD:'+_DB_PSSWD)
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
            if self.debug_mode:
                print("DB Connected!!")
        except Exception as e:
            if self.debug_mode:
                print("SF_DB connect Exception:\n", e)
            time.sleep(0.1)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return ret
        if self.debug_mode:
            print("Post input string to DB SP")

        sql = '''
    DECLARE @ReturnValue varchar(2000)
    EXEC %s '%s','%s','%s','%s','%s','%s','%s','%s','%s'
    SELECT @ReturnValue ''' % ('SP_Diagnose_SaveResultNew', sn, station, "F12", result, inputstring, "##", "", "", "")  # SP_Diagnose_SaveResultNew
        # print sql
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
            # outputstring = cur.fetchall()[0]
            cur.close()
            outputstring = result

            for res in result:
                if self.debug_mode:
                    print(res)
                    # print i
                    # i=i+1
                for (k, v) in res.items():
                    ret[k] = v
                    if self.debug_mode:
                        print("dict[{}] = {}".format(k, v))

            self.conn.commit()
            if self.debug_mode:
                print("SF_MSG = {}".format(outputstring))
        except Exception as e:
            if self.debug_mode:
                print("SF_DB Operate Exception:\n", e)
        self.conn.close()
        if self.debug_mode:
            print("SF DB Closed")
        return ret

    def MonitorPortal(self, bu, station, step, inputstring):
        ret = {}
        if self.debug_mode:
            print("start")
        try:
            if self.debug_mode:
                print("Connect SF_DB")
            self.conn = pymssql.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                login_timeout=30)
            if self.debug_mode:
                print("DB Connected!!")
        except Exception as e:
            if self.debug_mode:
                print("SF_DB connect Exception:\n", e)
            time.sleep(2)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = str(e)
            return ret
        if self.debug_mode:
            print("Post input string to DB SP")

        sql = '''
    DECLARE @ReturnValue varchar(2000)
    EXEC %s '%s','%s','%s','%s',@ReturnValue output
    SELECT @ReturnValue ''' % ('MonitorPortal', bu, station, step, inputstring)
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
            # outputstring = cur.fetchall()[0]
            cur.close()
            outputstring = result

            for res in result:
                if self.debug_mode:
                    print(res)
                    # print i
                    # i=i+1
                for (k, v) in res.items():
                    ret[k] = v
                    if self.debug_mode:
                        print("dict[{}] = {}".format(k, v))

            self.conn.commit()
            if self.debug_mode:
                print("SF_MSG = {}".format(outputstring))
        except Exception as e:
            if self.debug_mode:
                print("SF_DB Operate Exception:\n", e)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = str(e)
            self.conn.close()
            return ret
            # self.conn = None
        self.conn.close()
        if self.debug_mode:
            print("SF DB Closed")
        return ret

    def ParseKeyValuePairs(self, data, remove_set_prefix=False, msdb=False):
        """Parses key/value pairs in a request/response file.

        Invalid lines are logged and ignored.

        Args:
            data: An input string, e.g., 'A=B\nC=D\n'
            remove_set_prefix: If True, the prefix "set " (case-insensitive)
            is removed from each line.
        msdb: If True, response data get from backend directly. instead of
            send request file and get response file.

        Returns:
            A dictionary, e.g., {'A': 'B', 'C': 'D'}
        """
        ret = {}
        # Use split('\r\n') rather than splitlines(); we want to be strict
        # (as is the real backend).
        sep = ';' if msdb else '\r\n'
        for line in filter(None, data.split(sep)):
            if remove_set_prefix:
                line = re.sub(r'(?i)^set ', '', line)
            key, equals, value = line.partition('=')
            if equals:
                if len(value.strip()) > 0:  # remove have empty value keys
                    ret[key] = value
            else:
                logging.error('Invalid line %r', line)
        return ret
    def SP_Diagnose_Compare(self, sn,value,key,station_name, line):
            ret = {}
            inputstring = 'SN=' + sn + ';LINE=' + line + ';STATION=' + station_name + ';TYPE=SAVE' + key + ';' + key + '=' + value
            if self.debug_mode:
                print("start")
            try:
                if self.debug_mode:
                    print "Connect SF_DB"
                # print('_DB_SERVER:'+_DB_SERVER+'_DB_NAME:'+_DB_NAME+'_DB_USER:'+_DB_USER+'_DB_PSSWD:'+_DB_PSSWD)
                self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
                if self.debug_mode:
                    print "DB Connected!!"
            except Exception as e:
                if self.debug_mode:
                    print(("SF_DB connect Exception:\n", e))
                time.sleep(0.1)
                ret['RESULT'] = 'FAIL'
                ret['iResult'] = 'FAIL'
                ret['iMessage'] = e
                return ret
            sql = '''
        DECLARE @return_value int 
        EXEC %s '%s'
        SELECT 'Return Value' = @return_value  ''' % ('SP_Diagnose_Compare',inputstring)

            #print sql
            try:
                cur = self.conn.cursor()
                cur.execute(sql)
                index = cur.description
                print(type(index))
                print(index)
                #print("index: %s" % index)
                result = []
                for res in cur.fetchall():
                    row = {}
                for i in range(len(index)):
                    row[index[i][0]] = res[i]
                result.append(row)
                # outputstring = cur.fetchall()[0]
                cur.close()
                outputstring = result

                for res in result:
                    if self.debug_mode:
                        print res
                        # print i
                        # i=i+1
                    for (k, v) in res.items():
                        ret[k] = v
                        if self.debug_mode:
                            print "dict[%s]=" % k, v

                self.conn.commit()
                if self.debug_mode:
                    print "SF_MSG = ", outputstring
            except Exception as e:
                if self.debug_mode:
                    print(("SF_DB Operate Exception:\n", e))
            self.conn.close()
            if self.debug_mode:
                print("SF DB Closed")
            return ret


class SqlHelperSMT(interfaceSQL):

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def GetConnect(self):
        if not self.database:
            raise(NameError, "Please config database first!")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset="utf8", login_timeout=30)
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "Connect database fail!")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.GetConnect()
        cur.execute(sql)
        index = cur.description
        result = []
        for res in cur.fetchall():
            row = {}
        for i in range(len(index)):
            row[index[i][0]] = res[i]
        result.append(row)
        self.conn.close()
        return result

    def ExecNonQuery(self, sql):
        cur = self.GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def getMAC(self, sn, type):
        self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, charset="utf8", login_timeout=30)
        cur = self.conn.cursor()
        sql = '''
            DECLARE @p1 varchar(1000)
            SET     @p1 = ''
            DECLARE @p2 varchar(1000)
            SET     @p2 = ''
            EXEC    usp_GetDataFromSMT  @Type = '%s',@SN='%s',@Result = @p1 output,@msg = @p2 output
            SELECT  @p1 as Result, @p2 as Msg
                    '''
        sql = sql % (type, sn)
        cur.execute(sql)
        result_set = cur.fetchall()
        cur.close()
        self.conn.commit()
        self.conn.close()
        return result_set

    def UpdateMAC(self, sn, mac, type):
        self.RecordtoSF(sn, type, mac)

    def RecordtoSF(self, sn, funName, funValue):
        ret = {}
        try:
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
        except Exception as e:
            time.sleep(0.1)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return ret
        command = 'MB_NUM=' + sn + ";$;" + 'Key_Type=' + funName + ';$;Key_Value=' + funValue
        print(command)
        sql = '''
        DECLARE @return_value int,@OutPutStr nvarchar(max)
        EXEC    @return_value = [dbo].MonitorPortal--[dbo].MonitorFCTReceiveKey
                @BU = 'PU10',
                @Station = 'BFT',
                @Step = 'SaveKeyValue',
                @InPutStr = '%s',
                @OutPutStr = @OutPutStr OUTPUT
        SELECT  @OutPutStr as N'@OutPutStr'

        SELECT  'Return Value' = @return_value
        ''' % (command)

        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            index = cur.description
            cccc = cur.fetchall()
            k = 0
            for item in index:
                ret[item[0]] = cccc[0][k]
                k += 1
            cur.close()
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            self.conn.close()
            self.conn = None
        return ret

    def CheckStatusSMT(self, sn, station):
        ret = {}
        try:
            # print('_DB_SERVER:'+_DB_SERVER+'_DB_NAME:'+_DB_NAME+'_DB_USER:'+_DB_USER+'_DB_PSSWD:'+_DB_PSSWD)
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
        except Exception as e:
            time.sleep(0.1)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return ret
        sql = '''
    DECLARE @ReturnValue varchar(2000)
    EXEC %s '%s','%s','%s','%s'
    SELECT @ReturnValue ''' % ('SP_RoutingCheck', sn, station, "", "")
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            index = cur.description
            cccc = cur.fetchall()
            k = 0
            for item in index:
                ret[item[0]] = cccc[0][k]
                k += 1
            cur.close()
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            self.conn.close()
            self.conn = None
        return ret

    def UpdateSFSMT(self, sn, station, result, inputstring, mLine=""):
        ret = {}
        try:
            if mLine == "":
                LINE_count = inputstring.find("LINE", 0, len(inputstring))
                if LINE_count != -1:
                    pound_count = inputstring.find("#", LINE_count, len(inputstring))
                    mLine = inputstring[LINE_count + len("LINE="):pound_count]

            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
        except Exception as e:
            time.sleep(0.1)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return ret

        sql = '''
        Declare @ReturnValue VARCHAR(3000)
        Declare @iResult VARCHAR(1)
        Declare @iMessage VARCHAR(100)

        EXEC %s @SN='%s',@LINE='%s',@station='%s', @TestResult='%s', @Path ='%s' ,@FileName='%s', @FixtureID='%s',@OperatorID='%s',
        @Result =@iResult OUTPUT,@msg=@iMessage OUTPUT ,@PortID='%s',@InPutStr=N'%s';
        SELECT  @iResult as N'iResult',@iMessage as N'iMessage'
        ''' % ('usp_TestResultSave', sn, mLine, station, result, "", "", "", "", "", inputstring)

        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            index = cur.description
            cccc = cur.fetchall()
            k = 0
            for item in index:
                ret[item[0]] = cccc[0][k]
                k += 1
            cur.close()
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            self.conn.close()
            self.conn = None
        return ret

    def getMAC(self, sn):  # noqa keep api
        self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, charset="utf8", login_timeout=30)
        cur = self.conn.cursor()
        sql = '''
            DECLARE @p1 varchar(1000)
            SET     @p1 = ''
            DECLARE @p2 varchar(1000)
            SET     @p2 = ''
            EXEC    usp_GetDataFromSMT  @Type = 'MAC',@SN='%s',@Result = @p1 output,@msg = @p2 output
            SELECT  @p1 as Result, @p2 as Msg
                    '''
        sql = sql % (sn)
        cur.execute(sql)
        result_set = cur.fetchall()
        cur.close()
        self.conn.commit()
        self.conn.close()
        return result_set

    def getIMEI(self, sn):
        self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, charset="utf8", login_timeout=30)
        cur = self.conn.cursor()
        sql = '''
            DECLARE @p1 varchar(1000)
            SET     @p1 = ''
            DECLARE @p2 varchar(1000)
            SET     @p2 = ''
            EXEC    usp_GetDataFromSMT  @Type = 'IMEI',@SN='%s',@Result = @p1 output,@msg = @p2 output
            SELECT  @p1 as Result, @p2 as Msg
                    '''
        sql = sql % (sn)
        cur.execute(sql)
        result_set = cur.fetchall()
        cur.close()
        self.conn.commit()
        self.conn.close()
        return result_set

    def getHWinfo(self, sn):
        self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, charset="utf8", login_timeout=30)
        cur = self.conn.cursor()
        sql = '''
            DECLARE @p1 varchar(1000)
            SET     @p1 = ''
            DECLARE @p2 varchar(1000)
            SET     @p2 = ''
            EXEC    usp_GetDataFromSMT  @Type = 'HWINFO',@SN='%s',@Result = @p1 output,@msg = @p2 output
            SELECT  @p1 as Result, @p2 as Msg
                    '''
        sql = sql % (sn)
        cur.execute(sql)
        result_set = cur.fetchall()
        cur.close()
        self.conn.commit()
        self.conn.close()
        return result_set

    def getPN(self, sn):
        self.conn = pymssql.connect(host=self.host, database=self.database,
                                    user=self.user, password=self.password, charset="utf8", login_timeout=30)
        cur = self.conn.cursor()
        sql = '''
            DECLARE @p1 varchar(1000)
            SET     @p1 = ''
            DECLARE @p2 varchar(1000)
            SET     @p2 = ''
            EXEC    usp_GetDataFromSMT  @Type = 'PN',@SN='%s',@Result = @p1 output,@msg = @p2 output
            SELECT  @p1 as Result, @p2 as Msg
                    '''
        sql = sql % (sn)
        cur.execute(sql)
        result_set = cur.fetchall()
        cur.close()
        self.conn.commit()
        self.conn.close()
        return result_set

    def getBTMAC(self, sn):
        self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, charset="utf8", login_timeout=30)
        cur = self.conn.cursor()
        sql = '''
            DECLARE @p1 varchar(1000)
            SET     @p1 = ''
            DECLARE @p2 varchar(1000)
            SET     @p2 = ''
            EXEC    usp_GetDataFromSMT  @Type = 'BTMAC',@SN='%s',@Result = @p1 output,@msg = @p2 output
            SELECT  @p1 as Result, @p2 as Msg
                    '''
        sql = sql % (sn)
        cur.execute(sql)
        result_set = cur.fetchall()
        cur.close()
        self.conn.commit()
        self.conn.close()
        return result_set

    def UpdateBTMAC(self, sn, mac):
        ret = {}
        try:
            self.conn = pymssql.connect(host=self.host, database=self.database, user=self.user, password=self.password, login_timeout=30)
        except Exception as e:
            time.sleep(0.1)
            ret['RESULT'] = 'FAIL'
            ret['iResult'] = 'FAIL'
            ret['iMessage'] = e
            return ret
        mac = 'MB_NUM=' + sn + ";$;" + 'Key_Type=BTMAC;$;Key_Value=' + mac
        print(mac)
        sql = '''
        DECLARE @return_value int,@OutPutStr nvarchar(max)
        EXEC    @return_value = [dbo].MonitorPortal--[dbo].MonitorFCTReceiveKey
                @BU = 'PU10',
                @Station = 'BFT',
                @Step = 'SaveKeyValue',
                @InPutStr = '%s',
                @OutPutStr = @OutPutStr OUTPUT
        SELECT  @OutPutStr as N'@OutPutStr'

        SELECT  'Return Value' = @return_value
        ''' % (mac)

        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            index = cur.description
            cccc = cur.fetchall()
            k = 0
            for item in index:
                ret[item[0]] = cccc[0][k]
                k += 1
            cur.close()
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            self.conn.close()
            self.conn = None
        return ret

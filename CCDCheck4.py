#!/usr/bin/evn python
#coding:utf-8
import json
import os
import SocketServer
import time
import logging
import re
from datetime import datetime
from ConnectDB import ConnectDB
from SQLHelper import SqlHelper
from Logger import Logger
import threading
import serial
import socket
from font_color import font_color

filepath = os.path.dirname( os.path.realpath(__file__) )
_SERIAL_ = ""
return_msg = ""
ProgramVersion = '1.0.0.0.1'
PCname = socket.gethostname()
#       使用正则表达式判断SN格式，ip和端口写到配置档，删除多余配置档数据，删除多余的变量、方法、判断，导入离线控制   ——Young 2021/6/26

Logger = Logger()
class echorequestserver( SocketServer.BaseRequestHandler ):

    def handle( self ):
        conn = self.request
        logging.debug( "Connection on port %s" % self.client_address[1] ) 
        client_data = ""
        config_path = 'config_CCDCheck4.json'
        with open(config_path, 'r') as f:
            data = json.load(f)
        self.Model_name = data['modelname']
        self.Station_name = data['stationname']
        self.img_type = data['img_type']
        self.img_min = data['img_min']
        self.img_path = data['img_path']      

        while True:
            client_data = conn.recv( 1024 )
            client_data = client_data.decode('utf-8').strip()
            print (client_data)
            if client_data[-1:] != "" :
                print ("I got the delimiter")
                logging.debug( client_data )
                nowtime = str( datetime.now() )
                logging.debug( "%s - Get Signal from PLC: %s" % ( nowtime, client_data ) )
                logging.debug( "------------Request Start---------------" )
                return_msg = self.Execute_request( client_data )
                nowtime = str( datetime.now() )
                logging.debug( "%s - Respond data: %s" % ( nowtime, return_msg ) )
                logging.debug( "------------Request Finished------------" )
                conn.sendall( return_msg )
                return_msg = ""
                client_data = ""
                # break


    def Execute_request( self, client_data ) :
        iResult=''
        result = ''
        global _SERIAL_
        colour=font_color()
        logging.debug( "Data: %s \nOn port %s " % ( client_data, self.client_address[1] ) )
        client_data = client_data.strip()
        logging.debug( "Data: %s \nOn port %s " % ( client_data, self.client_address[1] ) )

        if re.search('SN=P\\d{7}-\\d{2}-\\w{1}:SCI9\\w{11}' , client_data) != None:
            _SERIAL_ = client_data[3:]
            print("-----------Do Routing-----------")
            routingcheck = ConnectDB()
            ( iResult, iMessage, iParamAll ) = routingcheck.CheckRoutingFA( _SERIAL_ , self.Station_name, None, None )
            print('-----------iResult------------',iResult)
            if "PASS" in iResult.upper() and iMessage != "Shop Floor Disabled":
                params = routingcheck.ParseKeyValuePairs(iParamAll)
                self.Model_name = params['Model']
                return_msg = "OK,%s" % self.Model_name
            elif "PASS" in iResult.upper() and iMessage == "Shop Floor Disabled":
                return_msg = "OK,%s" % self.Model_name
            else:
                print ("-----------Do Routing FAIL-----------")
                print('Routing Message', iMessage)
                return_msg = "NG,%s" % self.Model_name
                colour.printRed(u'Routing Check FAIL! ! !\n'.encode('gb2312'))
            Logger.SetLogFileName( _SERIAL_, self.Model_name, self.Station_name )
            Logger.Write( 'SerialNumber: %s' % _SERIAL_ )
            Logger.Write( 'Model: %s ' % self.Model_name )
            Logger.Write( 'Station: %s' % self.Station_name )
            Logger.Write( 'iResult: %s' % iResult )
            Logger.Write( 'iMessage: %s' % iMessage )
            Logger.Write( 'iParamAll: %s' % iParamAll )
            print('Routing Message', iMessage)

        elif "YC" == client_data.upper() :
            self.InitialVariable()
            print('**************get YC**************')

        elif "RESULT" in client_data.upper() :
            img_num = self.Check_Img()
            if client_data.upper().find("RESULT=PASS")>=0 and img_num > self.img_min:
                print('&&&&&&&&&&&&&&&&&&&&&&&&')
                result = 'PASS'
            else:
                result = 'FAIL'
            handshake = ConnectDB()
            inputstring = "##ProgramVersion=%s##PCName=%s##%s##" % (ProgramVersion, PCname, client_data) 
            Logger.Write( 'UpdateToSF:' )
            Logger.Write( 'inputstring=%s' % inputstring )

            ( iResult2, iMessage2 ) = handshake.UpdateToFADB( _SERIAL_, self.Station_name, result, inputstring )
            if iResult2.upper() == "PASS" and result == 'PASS':
                return_msg = "PASS"
                print ("return_msg:",return_msg)
                colour.Show_pass()              
            else :
                return_msg = "FAIL"
                print ("return_msg:",return_msg)
                colour.Show_fail()
            Logger.Write('QMS Response:')
            Logger.Write('iResult=%s' % iResult2)
            Logger.Write('iMessage=%s' % iMessage2)
            Logger.MoveLogByResult( return_msg )
            self.InitialVariable()
        else:
            return_msg = ''
            print('CHECK client_data format!!!:%s' % client_data)

        return return_msg.encode( "utf-8" )


    def InitialVariable( self ) :
        _SERIAL_ = ""
        
        

class QSMC_TCP_Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__( self )
        self.result = None
        self.message = None
        config_path = 'config_CCDCheck4.json'
        with open(config_path, 'r') as f:
            data = json.load(f)
        ( self.address, self.port ) = ( data['ip'], data['ipport'])

    def run(self) :
        self.ServerUp()

    def ServerUp(self):
        LogFileDirectory = "%s%sLogFolder%s" % ( filepath, os.sep, os.sep )
        if not os.path.exists( LogFileDirectory ) :
            os.makedirs( LogFileDirectory )
        logFile = "%sServerLog_%s.log" % ( LogFileDirectory, time.strftime( "%Y_%m_%d_%H_%M_%S", time.localtime() ) )
        logging.basicConfig( filename = logFile, level = logging.DEBUG )
        logging.getLogger( "QSMC TCP Server" ).setLevel( logging.DEBUG )

        logging.info( "listening to http://%s:%d" % ( self.address, self.port ) )
        
        server = SocketServer.ThreadingTCPServer( ( self.address, self.port ), echorequestserver )
        print ("TCP Server up on %s, %d" % ( self.address, self.port ))
        server.serve_forever()

if __name__=='__main__':
    tcp=QSMC_TCP_Server()
    while True:
        tcp.ServerUp()

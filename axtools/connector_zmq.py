"""
The connector for ZeroMQ
This is the connector which will be the core message queue within the same machine

__author__ = "Alex Xiao <http://www.alexxiao.me/>"
__date__ = "2017-04-22"
__version__ = "0.2"

    Version:
        0.1 : implemented zeroMQ publish/ subscribe & server/client mode
        0.2 : added device for publish/ subscribe mode
        
"""
import zmq
import sys
import time
from threading import Thread
'''
    The device whcih exchanges messages between pub/sub
'''
class exchange_device(Thread):
    '''
        The device whcih exchanges messages between pub/sub
    '''
    def __init__(self,name='Exchanger',port_pub=12116,port_sub=12117,debug=False):
        Thread.__init__(self)
        self.name=name
        self.port_pub=port_pub
        self.port_sub=port_sub
        self.socket=None
        self.context=None
        self.debug=debug
        self.running=False
            
    def run(self):
        #try:
        context = zmq.Context()        
        # Socket facing clients
        if self.debug: print('Got context')
        frontend = context.socket(zmq.SUB)
        addr="tcp://*:"+str(self.port_pub)
        if self.debug: print('Tring to bind PUB at '+addr)
        frontend.bind(addr)

        frontend.setsockopt(zmq.SUBSCRIBE, b"")
        if self.debug: print('Waiting for PUB at '+addr)
        # Socket facing services
        backend = context.socket(zmq.PUB)
        if self.debug: print('Tring to bind SUB at '+addr)
        addr="tcp://*:"+str(self.port_sub)
        backend.bind(addr)
        if self.debug: print('Waiting for SUB at '+addr)
        try:
            self.running=True
            print(self.name+" is ONLINE")
            zmq.device(zmq.FORWARDER, frontend, backend)
        except Exception as e:
            print(self.name+" is having issues")
            print(e)
        finally:    
        #    pass
            print(self.name+" is OFFLINE")
            self.running=False
            frontend.close()
            backend.close()
            context.term()
        
class publisher():
    
    def __init__(self,host='tcp://127.0.0.1',port=12116,mode='device',debug=False):
        """
          The publisher
          
            Parameters:
                port: the port publisher/device is on
                mode: default to 'device' whcih use intermediary device 
                        otherwise bind to port
        """
        self.host=host
        self.port=port
        self.mode=mode
        self.socket=None
        self.context=None
        self.debug=debug
        self.connect()
        
    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        local_addr=self.host+':'+str(self.port)
        if self.mode=='device':
            self.socket.connect(local_addr)
        else:
            self.socket.bind(local_addr)
        
    def disconnect(self):
        self.socket.close()
        
        
    def send_string(self,topic,msg):
        if self.debug: print ('DEBUG: Publishing [',topic,'] ', msg)
        self.socket.send_string("%s %s" % (topic, msg))
class subscriber():
    
    def __init__(self,topic,host='tcp://127.0.0.1',port=12117,debug=False,code='UTF-8'):
        """
          The subscriber
          
            Parameters:
                port: the port publisher is on
        """
        self.CODE=code
        self.port=port
        self.topic=topic
        self.socket=None
        self.context=None
        self.DEBUG=debug
        self.host=host
        self.connect()
        
    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        local_addr=self.host+':'+str(self.port)
        self.socket.connect (local_addr)
        topicfilter = self.topic.encode(self.CODE)
        self.socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
        
    def disconnect(self):
        self.socket.close()
        
    def receive_string(self):
        string = self.socket.recv().decode(self.CODE)
        if self.DEBUG: 
            print ('DEBUG: Received raw message:',string)
        topic, messagedata = string.split(' ',1)
        if self.DEBUG: 
            print ('DEBUG: Received [',topic,'] ', messagedata)
        return messagedata

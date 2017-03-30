"""
The wapper of sockets for both server & client

__author__ = "Alex Xiao <http://www.alexxiao.me/>"
__date__ = "2017-03-13"
__version__ = "0.5"

"""
import socket
import sys,time
from Log import log
from threading import Thread
from exceptions import ProcessEndException
#To show threads
#import threading
#threading.enumerate()
class socket_server(Thread):
    """
        To open a socket server
        
        addr 
    """
    def __init__(self,addr,port,in_core_logic,socket_name='Socket_server'
                 ,backlog=None,init_fun=None):
        Thread.__init__(self)
        self.address=addr
        self.port=port
        self.socket_name=socket_name
        self.backlog=backlog
        log('Socket Server initing @'+addr+':'+str(port),self.socket_name,'Info')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        self.server_address = (self.address, self.port)
        #print >>sys.stderr, 'starting up on %s port %s' % server_address
        self.sock.bind(self.server_address)
        self.core_logic=in_core_logic
        self.running=True
        self.timeout=-1 #300
        self.available_check_interval=30
        self.thread_list=dict()
        self.max_connections=1
        if init_fun!=None:
            init_fun(self)
        
    
    def init_logic(self):#,*args,**kwargs):
        '''Method to be override
        Input:
            *args: list arguments
            **kwargs: key words arguments        
        '''
        #raise TypeError('Method not yet defined')
        pass
    
    #def thread_logic(in_fun):
    #    def wrapper(self,connection,client_address):
    #        th_name=str(client_address)
    #        log('Connection to '+th_name+' is set...',self.socket_name,'Info')
    #        # run the loop while the server is up and the thread has not been removed from thread list
    #        while self.running and th_name in list(self.thread_list):
    #            try:                    
    #                self.core_logic(self,connection,client_address)
    #            except ProcessEndException:
    #                log('Connection to '+th_name+' is closing...',self.socket_name,'Info')
    #            except Exception as e:
    #                log(str(e),self.socket_name,'Error')
    #            finally:
    #                connectoin.close()
    #                log('Connection to '+th_name+' has been closed',self.socket_name,'Info')
    #        return wrapper
    #
    #@thread_logic
    #def each_client_logic(self,connection,client_address):
    #    self.core_logic(self,connection,client_address)
    def each_client_logic(self,connection,client_address):
        th_name=str(client_address)
        log('Connection to '+th_name+' is set...',self.socket_name,'Info')
        # run the loop while the server is up and the thread has not been removed from thread list
        alive=True
        while alive and self.running and th_name in list(self.thread_list):
            try:                    
                self.core_logic(self,connection,client_address)
            except socket.timeout:
                log('Connection to '+th_name+' is timeout...',self.socket_name,'Error')
                alive=False
            except ProcessEndException:
                log('Connection to '+th_name+' is closing...',self.socket_name,'Info')
                alive=False
            except Exception as e:
                print(str(e))
                log(str(e),self.socket_name,'Error')
        connection.close()
        log('Connection to '+th_name+' has been closed',self.socket_name,'Info')
        #self.core_logic(self,connection,client_address)
    
    
    #def core_logic(self,connection,client_address):
    #    '''Method to be override'''
    #    raise TypeError('Method not yet defined')
    
    def stop(self):
        self.running=False
        log('Waiting for all connections to be closed...',self.socket_name,'Info')
        for th in list(self.thread_list):
            if self.thread_list[th].is_alive():
                self.thread_list[th].join() 
        log('All connections closed. server is stopped',self.socket_name,'Info')
        self.sock.close()
        
    def check_clean_up(self):
        connections_available_cnt=self.max_connections
        for th in list(self.thread_list):
            if self.thread_list[th].is_alive():
                connections_available_cnt-=1 
            else:
                log('Closing connections '+th,self.socket_name,'Info')
                del self.thread_list[th]
                #pass
        return connections_available_cnt
    
    def run(self):
        
        # Listen for incoming connections
        if self.backlog!=None:
            self.sock.listen(self.backlog)
        else:
            self.sock.listen()
        connections_available_cnt=self.max_connections
        while self.running:
            # Wait for a connection
            #print >>sys.stderr, 'waiting for a connection'
            if self.max_connections>0 and connections_available_cnt>0:
                connection, client_address = self.sock.accept()
                try:
                    #print >>sys.stderr, 'connection from', client_address
                    log('Connected by client:'+str(client_address),self.socket_name,'Info')
                    # Receive the data in small chunks and retransmit it
                    #while self.running:
                    #try:
                        #self.core_logic(connection, client_address)
                    if self.timeout>0:
                        connection.settimeout(self.timeout)
                    # Start a new thread for the connection
                    th=Thread(target = self.each_client_logic,args = (connection, client_address))                    
                    self.thread_list[str(client_address)]=th
                    th.start()
                #except ProcessEndException:
                    #self.running=False

                except Exception as e:
                    log(str(e),self.socket_name,'Error')
                    #self.running=False
                #finally:
                    # Clean up the connection
                    #connection.close() 
                    #log('Socket Server Closed @'+self.address+':'+str(self.port),self.socket_name,'Info')
            else:
                if self.max_connections>1:
                    log('Max connections reached, could not accept more',self.socket_name,'Warning')
            #run connections check
            connections_available_cnt=self.check_clean_up()
                    
            #set main socket thread to sleep
            time.sleep(self.available_check_interval)

    def send_line(self,conn,string, line_end='\n'):
        conn.sendall((string+line_end).encode())

    def read_line(self,conn,buffer_size=256, line_end='\n'):
        buffer = ''
        data = True
        while data:
            data = conn.recv(buffer_size)
            buffer += data.decode()
            while buffer.find(line_end) != -1:
                line, buffer = buffer.split(line_end, 1)
                yield line
        return
class socket_client():
    def __init__(self,addr,port,socket_name='Socket_client'):
        self.address=addr
        self.port=port
        self.socket_name=socket_name
        log('Socket client initing @'+addr+':'+str(port),socket_name,'Info')# Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        self.server_address = (addr, port)
        #print >>sys.stderr, 'connecting to %s port %s' % server_address
        self.sock.connect(self.server_address)
        self.sendall=self.sock.sendall
        self.send=self.sock.send
        
    def send_line(self,string,line_end='\n'):
        self.sendall((string+line_end).encode())
        
    def read_line(self,buffer_size=256, line_end='\n'):
        buffer = ''
        data = True
        while data:
            data = self.sock.recv(buffer_size)
            buffer += data.decode()
            while buffer.find(line_end) != -1:
                line, buffer = buffer.split(line_end, 1)
                yield line
        return
        
    def close(self):
        self.sock.close()

#socket_port=16319
#
##@socket_serverd('localhost',socket_port)
#def server_logic(self,connection, client_address):
#    for line in self.read_line(connection):
#        print('rec',line)
#        if line=='Stop':
#            raise ProcessEndException()
#
#
#
#server=socket_server('localhost',socket_port,server_logic)
#server.start()
#
#
##d=socket_client('localhost',socket_port)
#
#c=socket_client('localhost',socket_port)
#
#c.send_line('Stsop')
#
#
#
#
#c.send_line('Stop')
#
#t=server.thread_list["('127.0.0.1', 34418)"]
#t.is_alive()
#connections_available_cnt=server.max_connections
#for th in list(server.thread_list):
#    if server.thread_list[th].is_alive():
#        connections_available_cnt-=1 
#    else:
#        log('Closing connections '+th,server.socket_name,'Info')
#        del server.thread_list[th]
#
#server.thread_list
#
#import DB
#ca=DB.get_im_memory_share()
#
#ca.select('logs',' 1=1 order by id desc limit 10')

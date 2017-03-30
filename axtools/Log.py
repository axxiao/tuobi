"""
The Log manager

Should be placed at <jupyter notebook root>/axtoools

__author__ = "Alex Xiao <http://www.alexxiao.me/>"
__date__ = "2017-02-08"
__version__ = "0.5"

"""
DEBUG=True
SQL_ERR_NoLogTable='no such table'
DAEMON_INTERVAL=600 #default to every 10 mins
DAEMON=True
DAEMON_STATUS='Init'
MAX_NUM_LOGS_RETAIN=50000
from DB import get_im_memory_share, Column
from tools import tryrun
import datetime,time
from threading import Thread
import queue
Q=queue.Queue()
class Logger(Thread):
    
    def __init__(self,queue):
        Thread.__init__(self)
        self.Q=queue
        
        
    def run(self):     
               
        cache=get_im_memory_share()
        self.log(cache,'Logger init...','System') 
        while DAEMON:
            while not self.Q.empty():
                #Get the items from queue and do log
                log_type,info,service=self.Q.get()
                #print(info,service,log_type)
                self.log(cache,info,service,log_type)
            time.sleep(1)
        self.log(cache,'Logger is stopped','System') 
        if DEBUG:
            print('Logger is stopped')
    
    def warp_time(self,in_time):
        return datetime.datetime.fromtimestamp(in_time).strftime('%Y-%m-%d %H:%M:%S')

    def log(self,cache,info,service=None,log_type='Info'):
        #curTS = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        curTS=self.warp_time(time.time())
        collist=['time','type','info','service']
        if service!=None:        
            if str(type(service))=="<class 'str'>":
                servicename=service
            else:
                servicename=service.name
        else:
            servicename='Unknown'
        inp=[(curTS,log_type,info,servicename)]

        rtn,rcode,rtype=cache.insert('logs',collist,inp)
        if rtype=='error':
            if SQL_ERR_NoLogTable in rtn.args[0]:
                #in case of log table has not been created yet, create the table
                if DEBUG:
                    print("Init, creating logs table")

                coldef=[Column(name='time',type='datetime',nullable=False),
                        Column(name='type',type='text',nullable=False),
                        Column(name='service',type='text',nullable=False),
                        Column(name='info',type='text',nullable=False)]
                cache.create_table('logs',coldef)
                cache.insert('logs',['time','type','service','info'],[(self.warp_time(time.time()),'Info','System','Table logs is created.')])
                cache.insert('logs',['time','type','service','info'],[(self.warp_time(time.time()),'Info','System',info)])
            else:
                if DEBUG:
                    print(rtn)
                raise ValueError(rtn[0].args)
                
def stop():
    global DAEMON
    DAEMON=False

def log(info,service=None,log_type='Info'):
    Q.put([log_type,info,service])        
def start_logger():
    global DAEMON
    logger=Logger(Q)
    DAEMON=True
    logger.daemon=True
    logger.start()
    return logger
class log_daemon(Thread):
    """
    The demon thread that make sure log prcoess working
    """
    def run(self):     
        self.cache=get_im_memory_share()
        
        while DAEMON:
            if DEBUG:
                print('Demon is checking...')
            log('Log Demon Checking...','Log Demon')
            global DAEMON_STATUS
            rtn,rcd,rtype=self.cache.run('select count(1) cnt from logs')
            #print(rtn)
            if rtype=='data':
                DAEMON_STATUS='Checking'
                cnum=rtn[0].cnt
                ENUM=(MAX_NUM_LOGS_RETAIN*2)
                if cnum>ENUM:
                    #purge data more than expected number
                    rtn,rcd,rtype=self.cache.run('select max(id) mid from logs')
                    smid=rtn[0].mid-MAX_NUM_LOGS_RETAIN
                    msg='Demon is cleaning up logs id less than '+str(smid)
                    
                    log(msg,'Log Demon')
                    sql='delete from logs where id<='+str(smid)
                    if DEBUG:
                        print(msg)
                        print(sql)
                    self.cache.run(sql)
            else:
                DAEMON_STATUS='Error'
                #raise ValueError('Unable to check logs table','Log Demon')
                log('[ERROR] Demon Failed, reason:'+rtn.args[0],'Log Demon','Error')
                
            DAEMON_STATUS='Sleepinng'    
                
            
            if DEBUG:
                print('Demon is going to sleep',DAEMON_INTERVAL/60,'minutes before next check.')
            log('Log Demon Sleeping, will be awake in '+str(DAEMON_INTERVAL/60)+' minutes','Log Demon')
            time.sleep(DAEMON_INTERVAL)
        #End of process
        if DEBUG:
                print('Demon is stopped')
        log('Log Demon Stopped','Log Demon')
    
    
def start_daemon():
    global DAEMON
    DAEMON=True
    log('Log Demon Starting...','Log Demon')
    t=log_daemon()
    t.daemon=True
    t.start()
    return t
def start(dug=False):
    global logger,daemon,DEBUG
    DEBUG=dug
    logger=start_logger()
    daemon=start_daemon()
#logger.join()
#daemon.join()
start(False)

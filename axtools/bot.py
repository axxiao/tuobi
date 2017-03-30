from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import collections
import queue,traceback,sys
from threading import Thread
from Log import log
SQL_ERR_NoTable='no such table'
from DB import Column,get_im_memory_share
class bot:
    
    def __init__(self,token,in_queue=None,debug=False):        
        #Thread.__init__(self)
        self.DEBUG=debug
        self.CMD = collections.namedtuple('CMD', 'doc handler')
        self.cmd_list=dict()
        self.users=dict()
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        if in_queue==None:
            self.msgQ=queue.Queue()
        else:
            self.msgQ=in_queue
            #dispatcher.remove_handler(echo_handler)
        
        unknown_handler = MessageHandler(Filters.command, self.unknown_cmd)
        self.dispatcher.add_handler(unknown_handler)
        txt_handler = MessageHandler(Filters.text, self.proc_txt)
        self.dispatcher.add_handler(txt_handler)
        self.name=self.updater.bot.name
        self.id=self.updater.bot.get_me().id
        self.DB=get_im_memory_share()
        #dispatcher.remove_handler(echo)
        self.user_table_collist=['botid','user_name','user_id','user_first_name','user_last_name']
        self.user_table_def=[Column(name='botid',type='BIGINT',nullable=False),
                        Column(name='user_name',type='text',nullable=False),
                        Column(name='user_id',type='BIGINT',nullable=False),
                        Column(name='user_first_name',type='text',nullable=False),
                        Column(name='user_last_name',type='text',nullable=False)]
        if self.DEBUG:
            print('Bot inited')
            self.last_msg=None
        
    
    def proc_txt(self,bot, update):
        if self.DEBUG:
            print('processing text input')
            self.last_msg=update.message
        usr=update.message.from_user
        if not usr.name in self.users:
            #new user
            print('New user',usr.name)
            self.add_user(usr)
        chat_id=update.message.chat_id    
        input_type='text'
        content=update.message.text
        self.msgQ.put([usr.name,chat_id,input_type,content])
        if self.DEBUG:
            print('Proc_txt',usr.name,chat_id,input_type,content)
        #bot.sendMessage(chat_id=update.message.chat_id, text=rtn_text)
            
    def unknown_cmd(self,bot, update):
        if self.DEBUG:
            print('processing cmd input')
            self.last_msg=update.message
        usr=update.message.from_user
        if not usr.name in self.users:
                #new user
                self.add_user(usr)
        chat_id=update.message.chat_id    
        input_type='cmd'
        content=update.message.text
        self.msgQ.put([usr.name,chat_id,input_type,content])
        if self.DEBUG:
                print('Proc_cmd',usr.name,chat_id,input_type,content)

    def empty(self):
        return self.msgQ.empty()
    
    def get(self):
        if not self.msgQ.empty():
            yield self.msgQ.get() 
            
    def reply(self,chat_id, msg):
        self.updater.bot.send_message(chat_id ,msg)
        
    def start(self,send_info=True,DB_URI=None):
        if DB_URI!=None:
            #use the provided one
            self.DB=DB(SHARE_PATH,DB_URI=True)       
        if self.updater.running:
            if self.DEBUG:
                print('Found running session, killing...')
            self.updater.stop()     
        #loading existing user info
        rtn,cnt,typ=self.DB.create_table('bot_users',self.user_table_def,True)
        if typ=='error':
                raise ValueError(rtn[0].args)
                if self.DEBUG:
                    print(rtn[0].args)
        rtn,cnt,typ=self.DB.select('bot_users','botid='+str(self.id))
        if typ=='error':
                raise ValueError(rtn[0].args)
                if self.DEBUG:
                    print(rtn[0].args)
        for row in rtn:
            self.users[row.user_name]=row.user_id
        
        self.updater.start_polling()
        if send_info:
            info=self.name+' is back online'
            for usr in self.users:
                self.reply(self.users[usr],info)
        if self.DEBUG:
            print(self.name,'is online')
        
    def stop(self,send_info=True):
        if send_info:
            info=self.name+' is offline'
            for usr in self.users:
                self.reply(self.users[usr],info)
        self.updater.stop()

    def register_cmd(self,cmd,fun,override=False):
        '''
             The function of register a new command

             Input:
                 cmd: the command
                 fun: function for the command
                 override: [optional] default to False, allow to override existing

        '''
        if cmd in self.cmd_list and not override:
            raise ValueError('[Error] Command is in list, override flag is not set to True to override')
        else:

            if fun.__doc__==None:
                raise ValueError('[Error] Function doc missing, please provide')
            if cmd in self.cmd_list:
                self.dispatcher.remove_handler(self.cmd_list[cmd].handler)
            cmd_handler = CommandHandler(cmd,fun)
            self.cmd_list[cmd]=self.CMD(doc=fun.__doc__ ,handler=cmd_handler)
            self.dispatcher.add_handler(cmd_handler)
     
    def add_user(self,usr):
        if self.DEBUG:
            print('Adding user',str(usr.name))
        try:
            self.users[usr.name]=int(usr.id)
            inp=[(  int(self.id),
                    str(usr.name),
                    int(usr.id),
                    str(usr.first_name),
                    str(usr.last_name)
                )]

            rtn,code,typ=self.DB.create_table('bot_users',self.user_table_def,True)
            print(rtn,code,typ)
            if typ=='error':
                raise ValueError(rtn[0].args)
            if self.DEBUG:
                print('Bot_users table is ready',str(usr.name))
            rtn,code,typ=self.DB.insert('bot_users',self.user_table_collist,inp)
            if typ=='error':
                raise ValueError(rtn[0].args)
            if self.DEBUG:
                print('Added user',str(usr.name))
        except Exception as e:
            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(repr(traceback.format_tb(exc_traceback)))
            if self.DEBUG:
                print('Failed to add user',str(usr.name),'Reason',str(e))
        


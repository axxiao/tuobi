"""
The DB tools for Sqlite 3

__author__ = "Alex Xiao <http://www.alexxiao.me/>"
__date__ = "2017-02-08"
__version__ = "0.5"

"""
import sqlite3
import collections
#conn = sqlite3.connect('example.db')
# to create in memory database use
#conn = sqlite3.connect(':memory:')
sqlite3.enable_shared_cache(True)
Column = collections.namedtuple('Column', ['name','type','nullable'])
Column.__new__.__defaults__ = (False,)


class DB:
    def __init__(self,dbname,**args):
        self.conn=None
        self.DB_NAME=dbname
        self.DEBUG=True
        self.conn = sqlite3.connect(self.DB_NAME,**args)

    def connect(self,**args):
        #file::memory:?cache=shared to open a shared DB
        #global DB_NAME, conn
        if self.conn!=None:
            #Try to check/ disconnect
            #TBC
            if self.DEBUG:
                print('Trying to check beforce connect')
        self.conn = sqlite3.connect(self.DB_NAME,**args)
        
    def disconnect(self):
        self.conn.close()

    def run(self,cmd,variables=None):
        """
        Run the DB command
        Input Parameters
            cmd: the actual command
            variables: [Optional] variables if any
        Output:
            Result set: [list of named tuple]
            Row  count: Integer
            Result Type: String data/ cmd/ error
        """   
        c=None
        try:
            c = self.conn.cursor()
            if variables!=None:
                c.executemany(cmd,variables)
            else:
                c.execute(cmd)   
            rtn=c.fetchall()
            cnt=len(rtn)
            rtype='data'
            if 'select' not in cmd.lower():
                self.conn.commit()  
                cnt=c.rowcount
                rtype='cmd'
            else:
                header=''
                for colheader in c.description:
                    header+=colheader[0]+' '
                RES=collections.namedtuple('Data',header.strip())
                rtno=rtn
                rtn=[]
                for cur in range(0,cnt):
                    #convert to namedtuple
                    rtn.append(RES(*rtno[cur]))
            if self.DEBUG:
                print(cnt,'rows')
        except Exception as e:
            rtype='error'
            rtn=e
            cnt=-2
            
        if c!=None:
            c.close()
        return rtn,cnt,rtype

    def create_list_of_tuple(self,headers=[],data=[],tupletype='Data'):
        """
        The function to create list of named tuple from normal tuple
        Inputs:
            headers: list of header names
            data: list of tuples
            tupletype [Optional]: The type name of the tuple, default to Data
        Output:
            the named tuple
        """
        rtn=[]
        RES=collections.namedtuple(tupletype,headers)
        for cur in range(0,len(data)):
                #convert to namedtuple
                rtn.append(RES(*data[cur]))    
        return rtn

    def create_table(self,tablename,coldef):
        """
        The default table creator, it will create table with id as primary which is auto incremental
        Input:
            tablename: the name of the table
            coldef: namedtuple of column definitions, e.g
                coldef=[Column(name='name',type='text',nullable=True),Column(name='type',type='CHARACTER(1)')]
        Output: N/A
        """

        stmt="create table "+tablename+'(ID INTEGER  PRIMARY KEY AUTOINCREMENT'
        for col in coldef:
            stmt+=','
            stmt+=col.name+' '+col.type
            if not col.nullable:
                stmt+=' NOT NULL '
        stmt+=')'
        rtn=self.run(stmt)
        index_stmt='CREATE INDEX '+tablename+'_main_index ON '+tablename+'(id)'
        return self.run(index_stmt)

    def insert(self,tablename,headers=[], data=[]):
        """
        Insert into table

        Inputs:
            tablename: the target table
            headers: the list of headers e.g. headers=['name','type']
            data: list of data e.g. data = [('Alex Xiao','A'),('Michael Ngo','N')]
        Output:
            Number of rows instered
        """

        stmt='INSERT INTO '+tablename+' ('
        c=0
        for col in headers:
            if c>0:
                stmt+=','
            stmt+=col
            c+=1
        stmt+=') VALUES (?'
        for num in range(1,len(data[0])):
            stmt+=',?'
        stmt+=')'
        return self.run(stmt, data)

    def select(self,tablename):
        return self.run('select * from '+tablename)
im_memory_share=DB("file:in_mem_db?mode=memory&cache=shared",uri=True)


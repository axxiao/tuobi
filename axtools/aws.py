
# coding: utf-8

# In[1]:
################################################################################
#
# The script to start/stop AWS instance according to config file
#
# By Alex Xiao
#
# Version: 0.1 19/01/2017 - Init version
#
# command line: python library to control AWS
#
# Key function 1. connect_AWS(config_file_name)
# 2. get_status() return instance id, status ,address, ip
# 3. start_AWS() return address
# 4. stop_AWS() return status
################################################################################
import boto3
import sys
import os
import time
MAX_CHECKS=30
OUT_Flag=False

# In[2]:

def request_vairable(var_name,info):
    var='NOT_SET'
    for arg in sys.argv:
            argin=(arg.lower()).strip()
            if var_name.lower() ==argin[:len(var_name)]:
                pos=arg.find('=')+1
                var=arg[pos:]
            break
    if var=='NOT_SET':
        var=input('Please set '+var_name+' value:'+info)
    return var


# In[3]:

def read_dict(line,params=dict()):
    #split the line and load file into dict
    pos=line.find('=')+1
    var_nm=line[0:pos-1]
    var_val=line[pos:]
    params[var_nm.strip()]=var_val.strip()


# In[4]:

def get_param(name,params,error_out_flg):
    val=params.get(name)
    if val==None and error_out_flg:
        #fail to get value
        raise ValueError('Failed to get value from KEY '+name)
    return val


# In[5]:

def set_Env_Var(name,value):
    if value!=None:
        os.environ[name] =value


# In[6]:

def get_status():
    status='UNKNONW'
    address='UNKNONW'
    ins_id='UNKNONW'
    ip='0.0.0.0'
    idesc = ec2.describe_instances()
    resp=idesc['Reservations']
    inslist=resp[0]['Instances']
    for ins in inslist:
        if INSTANCE_NAME==ins['KeyName']:
            status=ins['State']['Name']
            ins_id=ins['InstanceId']
            network=ins['NetworkInterfaces']
    if status=='running':
        #'running
        if OUT_Flag:
            print('Located instance',ins['KeyName'],'it is ',status)
        address=network[0]['Association']['PublicDnsName']
        ip=network[0]['Association']['PublicIp']
        if OUT_Flag:
            print('Address:',address)
    return ins_id,status,address,ip



# In[7]:

def connect_AWS(config_file_name):
    global INSTANCE_NAME
    global CHECK_INTERVAL
    global ec2

    params=dict()
    try:
        file=open(config_file_name
        , 'r')
        for line in file:
            read_dict(line,params)
    except:
        raise ValueError('Error when reading the file '+config_file_name+' please verify if the file is accessable')

    INSTANCE_NAME=get_param('AWS_NAME',params,True)
    ACCESS_KEY=get_param('ACCESS_KEY',params,True)
    SECRET_KEY=get_param('SECRET_KEY',params,True)
    REGION=get_param('REGION',params,True)
    CHECK_INTERVAL=int(get_param('CHECK_INTERVAL',params,True))
    set_Env_Var('HTTP_PROXY',get_param('HTTP_PROXY',params,False))
    set_Env_Var('HTTPS_PROXY',get_param('HTTPS_PROXY',params,False))
    set_Env_Var('AWS_CA_BUNDLE',get_param('AWS_CA_BUNDLE',params,False))
    ec2 = boto3.client(
    'ec2',
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
    ,region_name=REGION
    )


# In[8]:

def stop_AWS():
    #load_param(config_file_name)
    ins_id,status,address,ip=get_status()
    if status=='running':
        #if not started, try to start it
        print('Stopping instance ['+INSTANCE_NAME+']...')
        rtn=ec2.stop_instances(InstanceIds=[ins_id,])
    else:
        raise ValueError('ERROR: Instance '+INSTANCE_NAME+' is NOT running!')
        ins_id,status,address,ip=get_status() 
        cnt=0
        while status=='stopping':
        #wait for stopping
            cnt+=1
            time.sleep(CHECK_INTERVAL)
            print(' instance ['+INSTANCE_NAME+'] is in progress of stopping...')
            ins_id,status,address,ip=get_status() 
            if cnt>MAX_CHECKS:
                break; 
        if status=='stopped':
            print('Instance ['+INSTANCE_NAME+'] has been stopped')
        else:
            raise ValueError('ERROR: Failed to stop instance []'+INSTANCE_NAME+']')
    return status


# In[9]:

def start_AWS():
    ins_id,status,address,ip=get_status()
    if status!='running':
    #if not started, try to start it
        rtn=ec2.start_instances(InstanceIds=[ins_id,])
    time.sleep(CHECK_INTERVAL)
    ins_id,status,address,ip=get_status()
    if status!='running':
        raise ValueError('Failed to start the instance')
        #print(' instacne is started, address:')
        #print('INSTANCE_ADDRESS['+address+']')
    else:
        print(' instacne is up running, address:')
        print('INSTANCE_ADDRESS['+address+']')
    return address


# In[14]:

#Sample commands
#connect_AWS('d:\\server\\aws.config')
#print(get_status()) -> ('i-07071f287e4b9dd2a', 'running', 'ec2-13-55-173-25.ap-southeast-2.compute.amazonaws.com','13.55.173.25')
#print(start_AWS()) -> stopped
#print(stop_AWS()) -> ec2-13-55-173-25.ap-southeast-2.compute.amazonaws.com

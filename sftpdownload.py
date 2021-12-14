# -*- coding:utf-8 -*-
import paramiko
import os
import sys
import time
import datetime
class CONFIG_TEST():
    host = "192.168.23.151"
    username = 'mac'
    password = '123456'
    remot_dir = '/Users/mac/Desktop/'
    local_dir = '/Users/yanhaitao/Desktop/test/'
class CONFIG_PRD():
    host = ""
    username = ''
    password = '' 
    remot_dir = '/xlb/'
    local_dir = '/data1/' 

config = CONFIG_PRD

remot_dir = config.remot_dir
local_dir = config.local_dir

rows = 100000   #100000
flag = True

#sftp断点续传主方法
def sftp_download(sftp,filename,local_dir,remot_dir):
    print('in download!!!!!!!!!!~~~~~~~~~~~',filename)
    print('local_dir:!!@@@@@@',local_dir)
    files = os.listdir(local_dir)
    print(files)
    if filename in files:
        print('In resume downloading~~~~~~~~~~',filename)
        stat = os.stat(local_dir + filename)
        f_remote = sftp.open(remot_dir + filename)
        f_remote.seek(stat.st_size)
        print('hhHHHH:',local_dir + filename)
        f_local = open(local_dir + filename, 'ba')
        print('LLLLLLLLLL==========')
        tmp_buffer = f_remote.read(rows)
        print('RRRRRR==========')
        try:
            while tmp_buffer:
                buf = bytearray(tmp_buffer)
                print('11111',buf)
                f_local.write(buf)
                # time.sleep(1)
                # print('sleep 1sssssss')
                tmp_buffer = f_remote.read(rows)
        finally:
            f_local.close()
            f_remote.close()
    else:
        print('In Start Downloading~~~~~',filename)
        f_remote = sftp.open(remot_dir + filename)
        print(remot_dir + filename)
        f_local = open(local_dir + filename, "bw")
        tmp_buffer = f_remote.read(rows)  
        try:
            while tmp_buffer:
                buf = bytearray(tmp_buffer)
                # print('22222',buf)
                f_local.write(buf)
                # time.sleep(1)
                tmp_buffer = f_remote.read(rows)
        finally:
            f_local.close()
            f_remote.close()



def download_dir(local_dir,remot_dir,p_date):
    dir_exist = True if os.path.exists(local_dir) else False
    if not dir_exist:
        os.makedirs(local_dir)
    is_exist = True if p_date in os.listdir(local_dir) else False
    if not is_exist:
        print('There is not target Dir, mkdir:',local_dir + p_date)
        os.mkdir(local_dir + p_date)
    elif len(os.listdir(local_dir + p_date)) > 0:  #清除本地目标目录所有文件
        print('Files Before Cleaning:',os.listdir(local_dir + p_date))
        for file in os.listdir(local_dir + p_date):
            file_delete = os.path.join(local_dir,p_date,file)
            os.remove(file_delete)
        print('Files After Cleaning:',os.listdir(local_dir + p_date))
    flag = True
    while flag: # 断网时不断重试，直到成功为止。
        try:
            transport = paramiko.Transport((config.host,22))
            transport.connect(username=config.username,password=config.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            dirs = sftp.listdir(remot_dir)
            dirs_set = set(dirs)
            if p_date not in dirs_set:
                print('No Remote Dirs!')
                break
            reomte_files = sftp.listdir(remot_dir + p_date + '/')
            print('Len(reomte_files):',len(reomte_files))
            if len(reomte_files) == 0:
                print('No Remote Files!')
                break
            for filename in reomte_files:
                print('NNNNNNormal')
                remote_dir = remot_dir + p_date + '/'
                loc_dir = local_dir + p_date + '/'
                sftp_download(sftp,filename,loc_dir,remote_dir)
            flag = False  #所有文件传输完毕，停止循环。
        except paramiko.ssh_exception.SSHException as identifier:
            print("DownloadError")
            print('Exception:',identifier)
            flag = True
        except OSError as identifier: 
            print('Exception:',identifier)
            flag = True
    sftp.close()
    transport.close()

def main():
    startDay_s = '${START_DAY}'
    endDay_s = '${END_DAY}'
    startDay = datetime.datetime.strptime(startDay_s,'%Y-%m-%d')
    endDay = datetime.datetime.strptime(endDay_s,'%Y-%m-%d')
    while startDay < endDay:
        str_startDay = startDay.strftime('%Y-%m-%d')
        print('str_startDay:',str_startDay)
        download_dir(local_dir,remot_dir,str_startDay)
        delta = datetime.timedelta(days=1)
        startDay = startDay + delta

def main_test():
    transport = paramiko.Transport((config.host,22))
    transport.connect(username=config.username,password=config.password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    print(1111111)
    a = sftp.listdir('/')
    print(a)
    #sftp_download(sftp,'t1',local_dir+'2020-10-19/',remot_dir+'2020-10-12/')


if __name__ == '__main__':
    main()
    #main_test()

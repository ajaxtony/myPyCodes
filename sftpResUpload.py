# -*- coding:utf-8 -*-
# import config
import paramiko
import os
import sys
import time
import datetime
class CONFIG_TEST():
    host = "192.168.23.151"
    username = 'mac'
    password = '123456'
config = CONFIG_TEST 
rows = 1000   #100000
startDay = sys.argv[1]
endDay = sys.argv[2] 
print(startDay,endDay)
flag = True

remot_dir = '/Users/mac/Desktop/'
local_dir = '/Users/yanhaitao/Desktop/'

#sftp断点续传主方法
def sftp_upload(sftp,filename,local_dir,remot_dir):
    print('in upload!!!!!!!!!!~~~~~~~~~~~',filename)
    file_list = sftp.listdir(remot_dir)
    if filename in file_list:
        stat = sftp.stat(remot_dir + filename)
        f_local = open(local_dir + filename)
        f_local.seek(stat.st_size)
        f_remote = sftp.open(remot_dir + filename, "a")
        tmp_buffer = f_local.read(rows)  
        while tmp_buffer:
            f_remote.write(tmp_buffer)
            time.sleep(1)
            tmp_buffer = f_local.read(rows)
        f_remote.close()
        f_local.close()
    else:
        f_local = open(local_dir + filename)
        print(local_dir + filename)
        f_remote = sftp.open(remot_dir + filename, "w")
        tmp_buffer = f_local.read(rows)  
        while tmp_buffer:
            f_remote.write(tmp_buffer)
            time.sleep(1)
            tmp_buffer = f_local.read(rows)
        f_remote.close()
        f_local.close()



def upload_dir(local_dir,remot_dir,p_date):
    local_files = os.listdir(local_dir + p_date + '/')
    print(local_files)
    for filename in local_files:
        flag = True
        while flag: # 断网时不断重试，直到成功为止。
            try:
                transport = paramiko.Transport((config.host,22))
                transport.connect(username=config.username,password=config.password)
                sftp = paramiko.SFTPClient.from_transport(transport)
                print(1111111,p_date)
                is_exist = True if p_date in sftp.listdir(remot_dir) else False
                if not is_exist:
                    print(222222222222)
                    sftp.mkdir(remot_dir + p_date)
                print('NNNNNNormal')
                remote_dir = remot_dir + p_date + '/'
                loc_dir = local_dir + p_date + '/'
                print(remote_dir,'@@@',loc_dir)
                sftp_upload(sftp,filename,loc_dir,remote_dir)
                flag = False
            except paramiko.ssh_exception.SSHException as identifier:
                print("UUUUploadError")
                print('Exception:',identifier)
                flag = True
            except OSError as identifier: 
                print('Exception:',identifier)
                flag = True
    sftp.close()
    transport.close()

def main():
    startDay = datetime.datetime.strptime(sys.argv[1],'%Y-%m-%d')
    endDay = datetime.datetime.strptime(sys.argv[2],'%Y-%m-%d')
    # print(startDay,endDay)
    while startDay <= endDay:
        str_startDay = startDay.strftime('%Y-%m-%d')
        print(str_startDay)
        upload_dir(local_dir,remot_dir,str_startDay)
        delta = datetime.timedelta(days=1)
        startDay = startDay + delta


if __name__ == '__main__':
    main()



import paramiko
from globalvar import HOME_PATH
trans = paramiko.Transport(("192.168.1.101", 8888))
    # 建立连接
trans.connect(username="sysadm", password="Zxbdt@729.TTU")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh._transport = trans

sftp = ssh.open_sftp()

file_name = "test.txt"
# sftp.put(localpath=localpath, remotepath=remotepath)
sftp.put("./templates/"+file_name, HOME_PATH + file_name)
    
    
import paramiko
import bar
from log import logger
import jinja
from globalvar import config, HOME_PATH
import globalvar

# trans = None
sftp = None

RC_LOCAL_PATH = "/etc/rc.local"

def login(config_file):

    config.read(config_file, encoding='utf-8')
    ssh_username = config["DEFAULT"]["ssh_username"]
    logger.debug("username is {}".format(ssh_username))
    globalvar.ssh_password = config["DEFAULT"]["ssh_password"]
    logger.debug("password is {}".format(globalvar.ssh_password))

    ssh_ip = config["DEFAULT"]["ssh_ip"]
    logger.debug("ip is {}".format(ssh_ip))
    ssh_port = int(config["DEFAULT"]["ssh_port"])
    logger.debug("port is {}".format(ssh_port))

    trans = paramiko.Transport((ssh_ip, ssh_port))
    # 建立连接
    trans.connect(username=ssh_username, password=globalvar.ssh_password)
    bar.printStatus("ssh 登陆")
    return trans


def setup_SDK(trans):
    """[summary]

    Args:
        config ([type]): [配置文件]
        logger ([type]): [日志输出]
    """
    # 实例化一个transport对象

    # 将sshclient的对象的transport指定为以上的trans
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = trans
    # 执行命令，和传统方法一样
    # ssh_command('df -hl', logger)

    # 实例化一个 sftp对象,指定连接的通道
    global sftp
    # sftp = paramiko.SFTPClient.from_transport(trans)
    sftp = ssh.open_sftp()

    file_name = "sdk_install.tgz"
    # sftp.put(localpath=localpath, remotepath=remotepath)
    sftp.put("./templates/sdk_install.tgz", HOME_PATH + file_name)
    # sftp.close()
    target="/opt/sdk_install.tgz"

    #now move the file to the sudo required area!
    stdin, stdout, stderr = ssh.exec_command(
        "sudo -S -p '' mv {} {}".format(HOME_PATH+file_name, target))
    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()


    # ssh_sendfile(localpath='./11.txt', remotepath='/tmp/22.txt')
    # cmd = "pwd"
    # ssh_command(cmd, True)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = trans
    cmd = "sudo -S -p '' tar -zxf /opt/sdk_install.tgz -C /opt"
    # ssh_command(ssh, cmd, True)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # print(stdout.read().decode())
    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()


    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = trans
    cmd = "cd /opt;sudo -S -p '' ./install_ssal_sdk.sh"
    # ssh_command(ssh, cmd, True)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # print(stdout.read().decode())

    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = trans

    cmd = "sudo -S -p '' chmod 755 /sdk"
    # ssh_command(ssh, cmd, True)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # print(stdout.read().decode())

    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()


    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = trans
    str = "/bin/bash /sdk/start_ssal_sdk.sh & "
    cmd = 'sudo -S -p "" sed -i "/{}/i\{}" {}'.format(
        "exit 0", str, RC_LOCAL_PATH)
    # ssh_command(ssh, str)
    # print(str)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()
    # ssh_sed(ssh, , str, RC_LOCAL_PATH)

    bar.printStatus("SDK 安装...")

    # 发送文件
    # sftp.put(localpath='./11.txt', remotepath='/tmp/22.txt')
    # 下载文件
    # sftp.get(remotepath, localpath)

    # # 执行命令，和传统方法一样
    # stdin, stdout, stderr = ssh.exec_command('ls /tmp/22.txt')
    # print(stdout.read().decode())

    # ssh.close()


def ssh_command(ssh, cmd,  output=False):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    logger.debug("run command is {}".format(cmd))
    if output:
        print(stdout.read().decode())
    if stderr:
        print(stderr.read().decode())
    # if stdin:
    #     print(stdin.read().decode())


def ssh_sendfile(localpath, remotepath):
    sftp.put(localpath=localpath, remotepath=remotepath)


def ssh_getfile(localpath, remotepath):
    sftp.get(remotepath=remotepath, localpath=localpath)


def ssh_sed(ssh, find, insert, filename):
    """[在指定搜索的文字的位置之上插入一行文字]

    Args:
        find ([type]): [查找的字符串]
        replace ([type]): [需要加入的字符串]
        filename ([type]): [文件名称]
    """
    str = 'sudo -S -p '' sed -i "/{}/i\{}" {}'.format(find, insert, filename)
    # ssh_command(ssh, str)
    # print(str)
    stdin, stdout, stderr = ssh.exec_command(str)
    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()

def read_sysconf():
    config.read("./configs/template.cfg", encoding='utf-8')
    ip = config["sysConfig"]["ip"]
    port = int(config["sysConfig"]["port"])
    return {"ip": ip, "port": port}

def read_paramfile():
    config.read("./configs/template.cfg", encoding='utf-8')
    host = config["paramFile"]["host"]
    port = int(config["paramFile"]["port"])
    return {"host": host, "port": port}

def read_config_ssal(id):
    """获得文件的配置信息

    Returns:
        [type]: [description]
    """
    config.read("./configs/template.cfg", encoding='utf-8')
    gw_ip = config["DEFAULT"]["gw_ip"]
    gw_port = int(config["DEFAULT"]["gw_port"])
    dst_ip1 = config["DEFAULT"]["dst_ip1"]
    dst_port1 = config["DEFAULT"]["dst_port1"]
    local_ip1 = config["DEFAULT"]["local_ip1"]
    local_port1 = int(config["DEFAULT"]["local_port1"])
    dst_ip2 = config["DEFAULT"]["dst_ip2"]
    dst_port2 = config["DEFAULT"]["dst_port2"]
    local_ip2 = config["DEFAULT"]["local_ip2"]
    local_port2 = int(config["DEFAULT"]["local_port2"])
    return {
        "id":id,
        "gw_ip": gw_ip,
        "gw_port": gw_port,
        "dst_ip1": dst_ip1,
        "dst_port1": dst_port1,
        "local_ip1": local_ip1,
        "local_port1": local_port1,
        "dst_ip2": dst_ip2,
        "dst_port2": dst_port2,
        "local_ip2": local_ip2,
        "local_port2": local_port2,
    }


def set_ssal_conf(trans, id):
    """set ssal_conf file
    """
    filename = "ssal_conf.json"
    dict = read_config_ssal(id)
    jinja.renderfile(
        filename + ".j2", filename, dict)

    ssh_sendfile("./target/" + filename, HOME_PATH + filename)
    path="/sdk"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = trans
    stdin, stdout, stderr = ssh.exec_command(
        "sudo -S -p '' cp -rf {} {}".format(HOME_PATH + filename,path))
    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()
    bar.printStatus("ssal_conf.json 安装")


def set_paramFile(trans):
    filename = "paramFile"
    dict = read_paramfile()
    jinja.renderfile(
        filename + ".j2", filename, dict)
    path = "/data/app/SCMQTTIot/configFile/paramFile"

    # ssh_sendfile("./target/" + filename, path)
    ssh_sendfile("./target/" + filename, HOME_PATH + filename)


    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = trans
    stdin, stdout, stderr = ssh.exec_command(
        "sudo -S -p '' rm -rf {}".format(path))
    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = trans
    stdin, stdout, stderr = ssh.exec_command(
        "sudo -S -p '' mv {} {}".format(HOME_PATH+filename, path))
    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()


    bar.printStatus(filename+" 安装")


def set_sysConf(trans):
    filename = "sysConf.yaml"
    dict = read_sysconf()
    jinja.renderfile(
        filename + ".j2", filename, dict)

    path="/etc/"+filename
    ssh_sendfile("./target/" + filename, HOME_PATH + filename)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = trans
    stdin, stdout, stderr = ssh.exec_command(
        "sudo -S -p '' cp -rf {} {}".format(HOME_PATH + filename,path))
    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()
    bar.printStatus(filename+" 安装")


def renderfile(trans, id):
    set_ssal_conf(trans, id)
    set_sysConf(trans)
    set_paramFile(trans)

def addvpn(trans):
    config.read("./configs/template.cfg", encoding='utf-8')
    apn_name = config["wwan_vpn"]["apn_name"]
    pap_name = config["wwan_vpn"]["pap_name"]
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = trans
    stdin, stdout, stderr = ssh.exec_command("wwan apn add")
    stdin.write(apn_name + "\n")
    stdin.flush()
    stdin.write("\n")
    stdin.flush()
    stdin.write("\n")
    stdin.flush()
    stdin.write(pap_name + "\n")
    stdin.flush()
    stdin.write("0\n")
    stdin.flush()
    stdin.write("ppp-0\n")
    stdin.flush()
    bar.printStatus("vpn 安装")

def rebootSystem(trans):
    """发送系统重启命令

    Args:
        trans ([type]): [ssh trans]
    """
    str="sudo reboot"
    ssh = paramiko.SSHClient()
    ssh._transport = trans
    ssh_command(ssh, str)
    ssh.close()


def queryEsn(trans):
    """查询esn码

    Args:
        trans ([type]): [description]

    Returns:
        [type]: [description]
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = trans
    stdin, stdout, stderr = ssh.exec_command(
        "devctl -e")
    str = stdout.read().decode()
    code = str.split(":")[1]
    print("查询到ESN码:{}".format(code))
    return code


def pingmain(trans):
    """#主站ip地址
        main_ip=192.168.3.2
        #物管平台ip地址
        device_ip=172.16.4.70
    """
    config.read("./configs/system.cfg", encoding='utf-8')
    main_ip = config["DEFAULT"]["main_ip"]
    device_ip = config["DEFAULT"]["device_ip"]


    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = trans

    command = "ping -c 5 {}"


    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command.format(main_ip))
    bar.printStatus("测试主站:{}".format(main_ip))
    output = ssh_stdout.read().decode()
    error = ssh_stderr.read().decode()
    # print(output)
    if str(output).find('5 packets received') > 0:
        #这是绿色字体
        print("\033[32m测试主站成功!\033[0m")
    elif str(output).find('0 packets received') > 0:
        #这是红色字体
        print("\033[31;测试主站失败!\033[0m")
    
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(
        command.format(device_ip))
    bar.printStatus("测试物管平台:{}".format(device_ip))
    output = ssh_stdout.read().decode()
    error = ssh_stderr.read().decode()
    # print(output)
    if str(output).find('5 packets received') > 0:
        #这是绿色字体
        print("\033[32m测试物管平台成功!\033[0m")
    elif str(output).find('0 packets received') > 0:
        #这是红色字体
        print("\033[31;1m测试物管平台失败!\033[0m") 




if __name__ == "__main__":
    # logger = setup_logging("logs/", "main")
    # main()
    pass


# from ssh import ssh_command, ssh_sendfile
import configparser
from globalvar import config, HOME_PATH
import globalvar
import bar
import jinja
import paramiko


def read_config():
    config.read("./configs/template.cfg", encoding='utf-8')
    main_ip = config["SecurityProxyConfig"]["main_ip"]
    main_port = config["SecurityProxyConfig"]["main_port"]
    contain_ip = config["SecurityProxyConfig"]["contain_ip"]
    contain_port = config["SecurityProxyConfig"]["contain_port"]
    return {
        "main_ip": main_ip,
        "main_port": main_port,
        "contain_ip": contain_ip,
        "contain_port": contain_port
    }


def setup():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = globalvar.trans
    sftp = ssh.open_sftp()
    sftp.put("./templates/104param.json",
             HOME_PATH + "104param.json")
    filename = "104param.json"
    path = "/data/app/SCIEC104/configFile/"
    str = "sudo -S -p '' cp -rf {} {}".format(
        HOME_PATH+filename, path + filename)
    # print(str)
    stdin, stdout, stderr = ssh.exec_command(str)
    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()
    sftp.put("./templates/security.bin", HOME_PATH + "security.bin")
    bar.printStatus("安全文件安装")
    path = "/mnt/internal_storage/"
    filename = "security_proxy_config"
    dict = read_config()
    jinja.renderfile(
        filename + ".j2", filename, dict)

    sftp.put("./target/" + filename, HOME_PATH + filename)
    str = "sudo -S -p '' cp -rf {} {}".format(
        HOME_PATH+filename, path + filename)
    print(str)
    stdin, stdout, stderr = ssh.exec_command(str)
    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()
    bar.printStatus(filename + " 安装")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = globalvar.trans
    stdin, stdout, stderr = ssh.exec_command("sudo -S -p '' reboot")
    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()
    print("设备已经重新启动。。。")
    sftp.close()


def read_change_config():
    config.read("./configs/template.cfg", encoding='utf-8')
    main_ip = config["security_proxy_config_change"]["main_ip"]
    main_port = config["security_proxy_config_change"]["main_port"]
    contain_ip = config["security_proxy_config_change"]["contain_ip"]
    contain_port = config["security_proxy_config_change"]["contain_port"]
    return {
        "main_ip": main_ip,
        "main_port": main_port,
        "contain_ip": contain_ip,
        "contain_port": contain_port
    }


def change():

    path = "/mnt/internal_storage/"
    filename = "security_proxy_config"
    dict = read_change_config()
    jinja.renderfile(
        filename + ".j2", filename, dict)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh._transport = globalvar.trans
    sftp = ssh.open_sftp()

    sftp.put("./target/" + filename, HOME_PATH + filename)
    stdin, stdout, stderr = ssh.exec_command(
        "sudo -S -p '' cp -rf {} {}".format(HOME_PATH+filename, path + filename))
    stdin.write(globalvar.ssh_password + "\n")
    stdin.flush()
    bar.printStatus("修改安全配置文件")

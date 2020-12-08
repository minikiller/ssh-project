import security
import globalvar
from globalvar import config
import click
from util import setup_logging
import sys
import logging
from log import logger
import configparser
from time import sleep
import paramiko
import bar
import ssh
from globalvar import HOME_PATH


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    options_metavar="[options...]",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    default=False,
    show_default=True,
    help="Print debug messages.",
)
def rebootSystem(trans, pwd):
    """发送系统重启命令

    Args:
        trans ([type]): [ssh trans]
    """
    _str = "sudo -S -p '' reboot"
    ssh = paramiko.SSHClient()
    ssh._transport = trans
    stdin, stdout, stderr = ssh.exec_command(_str)
    stdin.write(pwd + "\n")
    stdin.flush()


def main(client_config="configs/system.cfg", debug=None):
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.info(f"Logging set to debug.")
    else:
        logger.setLevel(logging.INFO)
        logger.info(f"Logging set to info.")

    # ssh remote login
    # globalvar.trans = ssh.login(client_config)
    # while True:
    try:
        sleep(1)
        ip = input(
            "输入ip地址 : "
            "\n> "
        )
        login(client_config, ip)

    except KeyboardInterrupt:
        # initiator.stop()
        print("成功退出... !\n")
        sys.exit()
    except ValueError:
        # Handle the exception
        print('请输入数字!')


def login_remote(config_file, ip):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    ssh_username = config["DEFAULT"]["ssh_username"]
    logger.debug("username is {}".format(ssh_username))
    ssh_password = config["DEFAULT"]["ssh_password"]
    logger.debug("password is {}".format(globalvar.ssh_password))

    ssh_port = int(config["DEFAULT"]["ssh_port"])
    logger.debug("port is {}".format(ssh_port))

    trans = paramiko.Transport((ip, ssh_port))
    # 建立连接
    trans.connect(username=ssh_username, password=ssh_password)
    bar.printStatus("ssh 登陆")
    print("登录{}成功！".format(ip))
    return trans, ssh_password


def senderfile(trans, ip, ssh_password):
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

    file_name = "FE0"
    # sftp.put(localpath=localpath, remotepath=remotepath)
    # sftp.put("./templates/"+file_name, HOME_PATH + file_name)
    # sftp.close()
    # target = "/opt/sdk_install.tgz"
    # str = "sudo -S -p '' mv {} {}".format(HOME_PATH +
    #                                       file_name, "/etc/network/interfaces.d/FE0")
    # now move the file to the sudo required area!
    target = "/etc/network/interfaces.d/FE0"
    cmd = 'sudo -S -p "" sed -i "/{}/c\{}" {}'.format(
        "address "+ip, "address 192.168.1.101", target)

    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.write(ssh_password + "\n")
    stdin.flush()
    bar.printStatus("文件配置成功！")
    # _str = "sudo -S -p '' reboot"
    _str = "sudo service networking restart"
    ssh = paramiko.SSHClient()
    ssh._transport = trans
    stdin, stdout, stderr = ssh.exec_command(_str)
    stdin.write(ssh_password + "\n")
    stdin.flush()


def login(client_config, ip):
    """安装sdk程序
    """
    trans, ssh_password = login_remote(client_config, ip)
    senderfile(trans, ip, ssh_password)
    # rebootSystem(trans, ssh_password)
    print("设备已经重启")


if __name__ == "__main__":
    # logger = setup_logging("logs/", "client")
    main()

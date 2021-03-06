from time import sleep

import configparser
from log import logger
import logging
import sys
from util import setup_logging
import click
import ssh
from globalvar import config
import globalvar
import security


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
def main(client_config="configs/system.cfg", debug=None):
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.info(f"Logging set to debug.")
    else:
        logger.setLevel(logging.INFO)
        logger.info(f"Logging set to info.")

    # ssh remote login
    globalvar.trans = ssh.login(client_config)
    while True:
        try:
            sleep(1)
            choice = int(
                input(
                    "输入选项 :- "
                    "\n0. 退出"
                    "\n1. 安装SDK-1"
                    "\n2. 秘钥导入(将重启)"
                    "\n3. 修改安全代理文件"
                    "\n4. 查询ESN码"
                    "\n5. add vpn"
                    "\n6. 增加vpn通道"
                    "\n7. 修改回执文件"
                    "\n8. ping 主站测试"
                    "\n9. 重启设备"
                    "\n10. 删除sdk"
                    "\n11. 修复sdk问题"
                    "\n> "
                )
            )
            if choice == 1:
                # print("hahah ")
                installSdk(client_config, logger)
            elif choice == 2:
                # print("choice is two")
                installSecurity()
            elif choice == 3:
                changeSecurity()
            elif choice == 4:
                queryEsn()
            elif choice == 5:
                addvpn()
            elif choice == 6:
                createvpn()
            elif choice == 7:
                callback()
            elif choice == 8:
                pingmain()
            elif choice == 9:
                reboot()
            elif choice == 10:
                deleteSdk()
            elif choice == 11:
                installfile()
            elif choice == 0:
                print("成功退出... !\n")
                sys.exit()
            else:
                print("请重新选择!")

        except KeyboardInterrupt:
            # initiator.stop()
            print("成功退出... !\n")
            sys.exit()
        except ValueError:
            # Handle the exception
            print('请输入数字!')


def installSdk(client_config, logger):
    """安装sdk程序
    """
    ssh.setup_SDK(globalvar.trans)
    id = input("输入设备ID(只能5位):")
    ssh.renderfile(globalvar.trans, id)

 # 关闭连接
    # globalvar.trans.close()


def installfile():
    # id = input("输入设备ID(只能5位):")
    ssh.fixfile(globalvar.trans)


def installSecurity():
    security.setup()


def changeSecurity():
    security.change()


def addvpn():
    ssh.addvpn(globalvar.trans)


def queryEsn():
    ssh.queryEsn(globalvar.trans)


def pingmain():
    ssh.pingmain(globalvar.trans)


def createvpn():
    ssh.createvpn(globalvar.trans)


def callback():
    ssh.callback(globalvar.trans)


def reboot():
    ssh.rebootSystem(globalvar.trans)


def deleteSdk():
    ssh.deleteSdk(globalvar.trans)


if __name__ == "__main__":
    # logger = setup_logging("logs/", "client")
    main()

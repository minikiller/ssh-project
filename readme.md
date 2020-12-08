### 自动添加一行在匹配的行数

```
sed -i  "/exit/i\allow chengyongxu.com" hello.conf
```

> i 插入内容 sed ‘/匹配词/i\要加入的内容’ example.file 将内容插入到匹配的行目标的上一行位置）
> 在 exit 中插入 allow chengyongxu.com ，在 hello.conf 文件中

## process

### 1. ssh remote device

https://github.com/paramiko/paramiko

### 2. process bar

https://github.com/verigak/progress

### register

生成注册码

```
createCode()
```

### pyinstaller

```
pyinstaller --onefile main.py
```

### bug

Socket exception: 远程主机强迫关闭了一个现有的连接。 (10054)

###

wwan apn show dev all

###

```
sysadm@SCT230A:~$ sudo ls /sdk
[sudo] password for sysadm:
/sdk
sysadm@SCT230A:~$ sudo ls /sdk
/sdk
sysadm@SCT230A:~$ sudo rm -rf /sdk
sysadm@SCT230A:~$ sudo ls /sdk
bin  crypt  ssal_conf.json  start_ssal_sdk.sh
sysadm@SCT230A:~$
```

```
 ps -aux |grep saal
```

```
/bin/bash /sdk/start_ssal_sdk.sh &
exit 0
```

```
sudo netstat -nap|grep ssal 
```

```
pyinstaller --onefile main.py
```

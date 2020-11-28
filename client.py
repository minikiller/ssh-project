import paramiko

host="127.0.0.1"
port = 22
user="sunlf"
pwd="kalix.123"

try:
    client=paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host,port=port,username=user,password=pwd)
    while True:
        try:
            cmd=input("$> ")
            if cmd == "exit": break
            ssh_stdin, ssh_stdout, stderror = client.exec_command(cmd)
            
            ssh_stdin.write('1\n')
            ssh_stdin.flush()
            ssh_stdin.write('2\n')
            ssh_stdin.flush()
            # print(ssh_stdout.read().decode())
            # output = ssh_stdout.read()
            print(ssh_stdout.read().decode())
        except KeyboardInterrupt:
            break
        client.close()

except Exception as err:
    print(str(err))

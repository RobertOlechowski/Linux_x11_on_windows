import optparse
import os

def parse_comandline():
    parser = optparse.OptionParser()
    parser.add_option('-a', '--adress', action="store", dest="adress", help="ip adress")
    parser.add_option('-k', '--key', action="store", dest="key", help="ssh key file")
    parser.add_option('-u', '--user', action="store", dest="user", help="user name")
    parser.add_option('-c', '--command', action="store", dest="command", help="command to execute")
    options, args = parser.parse_args()

    targetIp, sshKey, user_name, target_command = options.adress, options.key, options.user, options.command
    import socket
    selfIP = socket.gethostbyname(socket.gethostname())
    selfIP = "192.168.10.126" # todo: fix it

    print("=======================================================")
    print('Self   IP : {}'.format(selfIP))
    print('Target IP : {}'.format(targetIp))
    print('user name : {}'.format(user_name))
    print('ssh   Key : {}'.format(sshKey))
    print('Command   : {}'.format(target_command))
    print("=======================================================")

    return targetIp, sshKey, user_name, target_command, selfIP


def is_online(host, timeout):
    import socket
    socket.setdefaulttimeout(timeout)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((host, 22))
        print("Host is On Line")
        s.close()
        return True
    except socket.error as e:
        print("Error on connect: %s" % e)
    s.close()
    return False


def _is_vcxsrv_runing():
    import subprocess
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if line.startswith(b"vcxsrv.exe"):
            #print (line)
            return True
    return False

def _start_vcxsrv(vcxsrv_path):
    import tempfile
    import subprocess

    scriptFile = tempfile.NamedTemporaryFile(prefix="x11_", suffix=".bat", delete=False)
    exe_name = os.path.join(vcxsrv_path, "xlaunch.exe")
    with open(scriptFile.name, 'w') as f:
        f.write("@start {} -run config/config.xlaunch".format(exe_name))

    scriptFile.file.close()
    ret = subprocess.check_call(scriptFile.name)
    os.remove(scriptFile.name)
    return ret

def _start_xhost(vcxsrv_path, targetIp):
    import time
    import subprocess


    MAX_TRY = 4
    exe_name = os.path.join(vcxsrv_path, "xhost")
    instruction = "{} +{}".format(exe_name, targetIp)

    for i in range(MAX_TRY):
        ret = subprocess.check_call(instruction)
        if ret == 0:
            return 0
        print("xhost problem try [{} of {}]".format(i, MAX_TRY))
        time.sleep(0.5)

    return 1

def call_aps(vcxsrv_path, targetIp):
    ret = 0
    if not _is_vcxsrv_runing():
        print("vcxsrv is NOT running")
        ret = _start_vcxsrv(vcxsrv_path)
        if ret == 0:
            print("vcxsrv Started")
    else:
        print("vcxsrv is already running")

    if ret != 0:
        return ret

    ret = _start_xhost(vcxsrv_path, targetIp)
    if ret != 0:
        print("xhost problem")
        return ret

    return 0

def executeCommand(command, targetIp, selfIp, user_name, sshKey):
    import paramiko

    export_display_command = "export DISPLAY={}:0".format(selfIp)

    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        ssh.connect(targetIp, 22, user_name, key_filename=sshKey)

        comand = "{} && {}".format(export_display_command, command)
        stdin, stdout, stderr = ssh.exec_command(comand)
        #res = stdout.read()
        #if len(res) > 0:
        #    print(res)

    finally:
        ssh.close()

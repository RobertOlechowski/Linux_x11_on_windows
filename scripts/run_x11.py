import optparse
import time
import lib
import sys

timeout = 0.5
waitTime = 4

vcxsrv_path = "D:/bin/VcXsrv"

targetIp, sshKey, user_name, target_command = lib.parse_comandline()

adressses = lib.get_ip_addresses()
selected = lib.select_ip(targetIp, adressses)
if selected == None:
    print("can't find self ip")
    sys.exit(1)

selfIP = selected
print("=======================================================")
print('Self   IP : {}'.format(selfIP))
print('Target IP : {}'.format(targetIp))
print('user name : {}'.format(user_name))
print('ssh   Key : {}'.format(sshKey))
print('Command   : {}'.format(target_command))
print("=======================================================")

if not lib.is_online(targetIp, timeout):
    sys.exit(1)

if lib.call_aps(vcxsrv_path, targetIp) != 0:
    print("Run server problem")
    sys.exit(1)


lib.executeCommand(target_command, targetIp, selfIP, user_name, sshKey)

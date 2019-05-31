import optparse
import time
import lib
import sys

timeout = 0.5
waitTime = 4

vcxsrv_path = "D:/bin/VcXsrv"

targetIp, sshKey, user_name, target_command, selfIp = lib.parse_comandline()


if not lib.is_online(targetIp, timeout):
    sys.exit(1)

if lib.call_aps(vcxsrv_path, targetIp) != 0:
    print("Run server problem")
    sys.exit(1)


lib.executeCommand(target_command, targetIp, selfIp, user_name, sshKey)

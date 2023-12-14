import os
import platform
import sys
import re
import subprocess
import GPUtil
import math
import psutil

osFlavor = platform.system()
if osFlavor != "Linux":
    print(f"Sorry, this program can not be run on {osFlavor} please use a Linux based OS instead.")
    sys.exit("osError")
osArch = platform.machine()
osProccesor = platform.processor()
osInfo = platform.freedesktop_os_release()
osDistro = osInfo["NAME"]
osBase = osInfo["ID_LIKE"]
osVer = osInfo["VERSION"]
def getCPU():
    command = "cat /proc/cpuinfo"
    all_info = subprocess.check_output(command, shell=True).decode().strip()
    for line in all_info.split("\n"):
        if "model name" in line:
            return re.sub( ".*model name.*:", "", line,1)
def getGPU():
    gpu = GPUtil.getGPUs()
    if gpu == []:
        return "No GPU found!"
    else:
        return gpu
def getRAM():
    command = "cat /proc/meminfo"
    all_info = subprocess.check_output(command, shell=True).decode().strip()
    for line in all_info.split("\n"):
        if "MemTotal" in line:
            cmd = int(re.sub( ".*MemTotal.*:", "", line,1).strip("kB").strip(" "))
            RAM = cmd * 1000
            return convert_size(RAM)
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])
def getDisks():
    d = psutil.disk_partitions()
    count = 0
    for each in d:
        l = d[count]
        device = l[0]
        mountpnt = l[1]
        fstype = l[2]
        return f"Disk: {count+1}\n   Device: {device}\n   Mount Point: {mountpnt}\n   Filesystem: {fstype}"
        count = count + 1
print(f"Linux Distro: {osDistro}\nBase: {osBase}\nVersion: {osVer}\nSystem Architecture: {osArch}\nCPU:{getCPU()}\nGPU: {getGPU()}\nTotal RAM: {getRAM()}\n")
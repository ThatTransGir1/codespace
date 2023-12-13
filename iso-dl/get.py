import requests
from colorama import Fore
import platform
import os
import validators
import sys
import gzip
import time

def download(url: str, fileName: str, dir:str):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    length = response.headers.get('content-length')
    block_size = 1000000  # default value
    if length:
        length = int(length)
        block_size = max(4096, length // 20)
    filesize = length*10**-6
    filesize = round(filesize, 2)
    print(Fore.BLUE+f"{fileName}"+Fore.RESET+' size: '+Fore.CYAN+f"{filesize} MB"+Fore.RESET)
    with open(dir+"/"+fileName, 'wb') as f:
        size = 0
        for buffer in response.iter_content(block_size):
            if not buffer:
                break
            f.write(buffer)
            size += len(buffer)
            if length:
                percent = int((size / length) * 100)
                print(Fore.RESET+"Downloading "+Fore.BLUE+f"{fileName} to "+Fore.LIGHTWHITE_EX+f"{dir}"+': '+Fore.CYAN+f"{percent}%", end='\r')
    print(Fore.GREEN+"\n\nDone Downloading: "+Fore.CYAN+f"{dir}/{fileName}"+Fore.RESET+'\n')

def start():
    i = input("┌──────────────────────────────────────────────────────────────────────────────────┐\n│　　　　　　　　　　　　　　　　　　 Welcome 　　　　　　　　　　　　　　　　　　 │\n│　　　This is a tool to download Ventoy and/or isos of popular linux distros 　　 │\n│　　　(if you are on linux you can also use it to create a bootable volume)　　　 │\n│　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　  │\n│　　　　　　　　　　　　　　　 [1]- Download Ventoy　　　　　　　　　　　　　　　 │\n│　　　　　　　　　　　　　　　　[2]- Download ISOS 　　　　　　　　　　　　　　　 │\n│[3]- Create bootable volume from ISO (requires sudo, can be run on mac and linux) │\n│　　　　　　　　　　　　　　　　　　[4]- Exit　　　　　　　　　　　　　　　　　　 │\n└──────────────────────────────────────────────────────────────────────────────────┘\n\n: ")
    if i == "1":
        vtoy()
    elif i == "2":
        main()
    elif i == "3":
        ""
    elif i == "4":
        sys.exit("Closing program")
    if int(i) >= 4:
        print("The number you entered is not a valid input, please enter a number between [1-4]")


def cdisk():
    if platform.system() == "Windows":
        print("Sorry but this cannot be run on windows, I reccomend you use RUFUS link: https://rufus.ie")
    print("WARNING\n\nThis is going to need to use SUDO and DD (disk destroyer) to flash the ISO onto the usb to make it bootable")
    os.system("lsblk --noheadings --nodeps --paths --raw --output NAME,RM,TRAN,TYPE | grep ' 1 usb disk$' | cut --delimiter ' ' --fields 1")
    print("above is a list of usb drives plugged into your system, copy (select the text and use ctrl/cmd+shift+c to copy the text)\nThe exact string (e.g /dev/sda) for use later in the procces")
    i = input("please paste the copied drive string here: ")
    a = input("please specify the path to the ISO file: ")
    cmd = "dd if="+a+" of="+i+" status=progress"
    x=input("Are you sure you want to write "+a+" to "+i+" the data currently on your usb drive will be completely erased [y/n]: ")
    

def vtoy():
    urls = ["https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-xfce.iso", "", "", ""]
    ventoy = ["https://github.com/ventoy/Ventoy/releases/download/v1.0.96/ventoy-1.0.96-linux.tar.gz", "https://github.com/ventoy/Ventoy/releases/download/v1.0.96/ventoy-1.0.96-windows.zip", "https://github.com/ventoy/Ventoy/releases/download/v1.0.96/ventoy-1.0.96-livecd.iso"]
    i = input("Would you like to download Ventoy [y/n]:\n")
    if i.lower() == "y":
        print("The program will now download Ventoy.\nIf you are running Windows/Linux it will run the script for you.\nIf you are using MacOS you will need to flash the CD image to a USB/DVD/SD Card.")
        if os.path.exists("ventoy") == False:
            os.mkdir("ventoy")
        if platform.system() == "Windows":
            download(ventoy[1],"ventoy-windows.zip","ventoy")
        if platform.system() == "Linux":
            download(ventoy[1],"ventoy-livecd.iso", "ventoy")
            print("Please insert the usb drive that you want Ventoy installed on. \nA usb drive of 16GB or more is reccomended as ISO files are large.")
            time.sleep(20.5); print("please wait while we find the usb drive")
            os.system("lsblk --noheadings --nodeps --paths --raw --output NAME,RM,TRAN,TYPE | grep ' 1 usb disk$' | cut --delimiter ' ' --fields 1")
            i = input("type the path of the usb drive that you want Ventoy installed on EXACTLY as it shows above: ")
            print("WARNING: this part of the program requires the use of sudo, procede at your own risk.")
            x = input("WARNING: this part of the program requires the use of dd (diskdestroyer) this will reformat the entire usb deive\n\nWould you like to continue [y/n]: ")
            if x.lower() == "y":
                c = input("Please confirm that you want to erase " + i + "and install ventoy")
                if c.lower() == "y":
                    os.system("sudo dd if=/ventoy/ventoy-livecd.iso of="+i+"status=progress")
                    print("Done, to complete the setup of ventoy please load the drive from your bios and follow the instructions provided.")
        if platform.system() == "Darwin":
            download(ventoy[2],"ventoy-livecd.iso","ventoy")
            print("You will need to use a program to flash this to a USB/DVD/SD Card. Balena Etcher is recommended.")

def main():
    if os.path.exists("output") == False:
        os.mkdir("output")
    os.system("clear")
    global i
    print("--------------------------------------------------\nWhat Operating System would you like to download.\nPlease select an option from below\nIf the OS you want to install is not on the list select other and specify the direct ISO image download url.\n--------------------------------------------------")
    i = input("\n[1]- Debian (you can select what flavor you want after you select this)\n[2]- Arch Linux\n[3]- Ubuntu\n[4]- Manjaro Linux (You can select the flavor you want after selecting this)\n[5]- Linux Mint (You can select the flavor you want after selecting this)\n[6]- Other\n\n: ")
    if i == "1":
        debiandl()
    elif i == "2":
        archdl()
    elif i == "3":
        ubuntudl()
    elif i == "4":
        manjarodl()
    elif i == "5":
        mintdl()
    elif i == "6":
        otherdl()
    if int(i) >= 6:
        print(i+" is not a valid option, please enter a valid number [1-6]")

def debiandl():
    os.system("clear")
    debian = ['https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-standard.iso','https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-cinnamon.iso','https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-gnome.iso','https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-kde.iso','https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-lxde.iso','https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-lxqt.iso','https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-mate.iso','https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-12.4.0-amd64-xfce.iso']
    print("What flavor of Debian do you want to download")
    d = input("[1]- Standard\n[2]- Cinnamon\n[3]- GNOME\n[4]- KDE Plasma\n[5]- LXDE\n[6]- LXQT\n[7]- MATE\n[8]- XFCE\n[9]- Back\n\nWhich one(if none is selected Standard will be downloaded):\n")
    if d == "":
        download(debian[0],"debian-standard.iso","output")
    elif d == "1":
        download(debian[0],"debian-standard.iso","output")
    elif d == "2":
        download(debian[1],"debian-cinnamon.iso","output")
    elif d == "3":
        download(debian[2],"debian-gnome.iso","output")
    elif d == "4":
        download(debian[3],"debian-kde-plasma.iso","output")
    elif d == "5":
        download(debian[4],"debian-lxde.iso","output")
    elif d == "6":
        download(debian[5],"debian-lxqt.iso","output")
    elif d == "7":
        download(debian[6],"debian-mate.iso","output")
    elif d == "8":
        download(debian[7],"debian-xfce.iso","output")
    elif d == "9":
        back()
    if int(i) >= 9:
        print(i+" is not a valid option, please enter a valid number [1-9]")
    
def archdl():
    os.system("clear")
    i = input("Would you like to download Arch Linux? [y/n]")
    if i.lower() == "y":
        arch = "https://www.mirrorservice.org/sites/ftp.archlinux.org/iso/2023.12.01/archlinux-2023.12.01-x86_64.iso"
        download(arch,"archlinux.iso","output")
    else:
        back()

def ubuntudl():
    os.system("clear")
    i = input("Would you like to download Ubuntu? [y/n]")
    if i.lower() == "y":
        ubuntu = "https://releases.ubuntu.com/22.04.3/ubuntu-22.04.3-desktop-amd64.iso?_ga=2.66606951.893221735.1702384350-1119187640.1701438487"
        download(ubuntu,"ubuntu.iso","output")
    else:
        back()

def manjarodl():
    os.system("clear")
    manjaro = ["https://download.manjaro.org/kde/23.0.4/manjaro-kde-23.0.4-231015-linux65.iso","https://download.manjaro.org/xfce/23.0.4/manjaro-xfce-23.0.4-231015-linux65.iso", "https://download.manjaro.org/gnome/23.0.4/manjaro-gnome-23.0.4-231015-linux65.iso"]
    print("what flavor of Manjaro Linux would you like to download")
    m = input("[1]- KDE Plasme\n[2]- XFCE\n[3]- Gnome\n[4]- Back\n\nWhich one(if none is selected Standard will be downloaded):\n")
    if m == "1":
        download(manjaro[0],"manjaro-kde.iso","output")
    elif m == "":
        download(manjaro[0], "manjaro-kde.iso","output")
    elif m == "2":
        download(manjaro[1], "manjaro-xfce.iso","output")
    elif m == "3":
        download(manjaro[2], "manjaro-gnome.iso","output")
    elif m == "4":
        back()
    if int(i) >= 4:
        print(i+" is not a valid option, please enter a valid number [1-4]")

def mintdl():
    os.system("clear")
    mint = ["https://mirrors.layeronline.com/linuxmint/stable/21.2/linuxmint-21.2-cinnamon-64bit.iso","https://mirrors.layeronline.com/linuxmint/stable/21.2/linuxmint-21.2-mate-64bit.iso","https://mirrors.layeronline.com/linuxmint/stable/21.2/linuxmint-21.2-xfce-64bit.iso"]
    print("What flavor of Linux Mint would you like to download")
    l = input("[1]- Cinnamon\n[2]- Mate\n[3]- XFCE\n[4]- Back\n\nWhich one(if none is selected Standard will be downloaded):\n")
    if l == "":
        download(mint[0],"linux-mint-cinnamon.iso","output")
    elif l == "1":
        download(mint[0],"linux-mint-cinnamon.iso","output")
    elif l == "2":
        download(mint[1],"linux-mint-mate.iso","output")
    elif l == "3":
        download(mint[2],"linux-mint-xfce.iso","output")
    elif l == "4":
        back()
    if int(i) >= 4:
        print(i+" is not a valid option, please enter a valid number [1-4]")

def otherdl():
    os.system("clear")
    i = input("Would you like to download your own iso? [y/n]: ")
    if i.lower() == "y":
        print("Please provide the EXACT link to the ISO file you would like to download")
        o = input("url:\n")
        if validators.url(0) == True:
            download(o,"other.iso","output")
        else:
            print("The url you entered was not valid")
    else:
        back()

def back():
    os.system("clear")
    main()

start()
import subprocess

def mount_usb():
    p = subprocess.Popen(['sudo','blkid'], stdout=subprocess.PIPE)
    subprocess.Popen(['sudo', 'umount', '/media/usb'], stdout=subprocess.PIPE)
    print("Unmounted /media/usb..")

    out, errors = p.communicate()
    out = out.decode('utf-8')
    print(out)
    num = len(out.split('\n'))

    mount = False
    for i in range(num-1):
        device = out.split('\n')[i].split()[0][:-1]

        device_list = ['sda', 'sdb', 'sdc']
        if any(s in device for s in device_list):
            try:
                print("Device: ", device)
                subprocess.Popen(['sudo', 'mount', device, '/media/pi/USB'], stdout=subprocess.PIPE)
                print("Successfully mounted device to /media/pi/USB directory.")
                mount = True
            except Exception as e:
                print("Error mounting USB drive..")
                raise TypeError(e)
    return mount

def main():
    print("USB drive mounting status: ", mount_usb())

if __name__ == '__main__':
    main()

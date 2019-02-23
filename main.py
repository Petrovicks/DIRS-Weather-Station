# Timekeeping.
import datetime
import ntplib

# System calls / directory manipulation
import os

# Bash scripting.
import subprocess

# Custom scripts.
from usb_mount import mount_usb
from BME280 import bme280_init
from test_wifi import internet_on

# RTC.
import DS1307

# Change these to change some of the code behavior.
DIR_TIME = 60 # Sets number of seconds before making a new directory.
LOCATION_PRESSURE = 1013.25 # Current location's air pressure in hPa.

def main():

    # TODO: Make this better.
    print("Mounting USB drive..")
    try:
        if(mount_usb()):
            print("Successfully mounted drive to /media/pi/USB.")
        else:
            print("Error mounting usb drive, exiting..")
            exit()
    except Exception as e:
        raise TypeError(e)

    print("Initializing BME280 sensors..")
    try:
        weather_sensors = bme280_init(LOCATION_PRESSURE)
        print("Successfully initialized weather sensors.")
    except Exception as e:
        raise TypeError(e)

    # Initialize RTC.
    real_time_clock = DS1307.DS1307(1, 0x68)

    # Sets RTC if internet is detected.
    if internet_on():
        print("Can open google.com; setting RTC to NTP time.")
        ntpc = ntplib.NTPClient()
        real_time_clock.write_datetime(datetime.datetime.utcfromtimestamp(ntpc.request('europe.pool.ntp.org').tx_time))
        print('RTC sucessfully set')
    else:
        print("No internet, using current RTC time.")

    totalTime = DIR_TIME + 1 # Ensures the "if" conditional will always fail on first ever iteration of while loop.
    while True: #Stuck forever.
        if totalTime > DIR_TIME:
            time_string = real_time_clock.read_str().replace("T", "_")
            start_time = int(time_string[-2:]) + int(time_string[-5:-3])*60
            fullDN = "/media/pi/USB/" + time_string.replace(":", "") # UNTESTED. Save to USB.
            #fullDN = time_string.replace(":", "")
            os.mkdir(fullDN)
            totalTime = 0
        time_string = real_time_clock.read_str().replace("T","_")
        time_a = int(time_string[-2:]) + int(time_string[-5:-3])*60

        # TODO: Switch to multithreading for better resource management.
        print("Taking picture..")
        file_name = fullDN + "/" + "pureTherm_" + real_time_clock.read_str().split("T")[1:][0]
        file_name = file_name.replace(":","")
        print(file_name)
        subprocess.Popen(['sudo','ffmpeg','-i', '/dev/video0','-compression_algo','raw','-vframes','1',file_name+".tiff"], stdout = subprocess.PIPE)

        # Take 0.2s video from camera mounted at /dev/video1
        print("Taking video from what is hopefully the TAMARISK 320")
        file_name = fullDN + "/" + "Tamarisk_" + real_time_clock.read_str().split("T")[1:][0]
        file_name = file_name.replace(":","")
        print(file_name)

        # How to take raw video with Tamarisk was no documented, one of these should work.
        subprocess.Popen(['sudo','ffmpeg','-i', '/dev/video1','-compression_algo','raw','-t','00:00:00.20',file_name+".avi"], stdout = subprocess.PIPE)
        #subprocess.Popen(['sudo','ffmpeg','-i', '/dev/video1','-f','rawvideo','-t','00:00:00.20',file_name+"avi"],stdout = subprocess.PIPE)

        #Take weather sensor readings
        path = file_name + ".txt"
        readings_file = open(path, 'w')
        readings_file.write("\nTemperature: %0.1f C" % weather_sensors.temperature)
        readings_file.write("\nHumidity: %0.1f %%" % weather_sensors.humidity)
        readings_file.write("\nPressure: %0.1f hPa" % weather_sensors.pressure)
        readings_file.write("\nAltitude = %0.2f meters" % weather_sensors.altitude)

        time_interval = 0
        current_time = 0

        # Enforce one second time interval between recordings.
        while(time_interval < 1):
#            print("everything: ", time_string)
#            print("seconds: ", time_string[-2:])
#            print("minutes: ", time_string[-5:-3])
            time_string = real_time_clock.read_str().replace("T", "_")
            current_time = int(time_string[-2:]) + int(time_string[-5:-3])*60
            time_interval = current_time - time_a
        totalTime = current_time - start_time

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise TypeError(e)

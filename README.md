This is a datalogger utilizing a Raspberry Pi 3B to grab an IR tiff 
image as well as read in sensing data from an all-purpose weather 
sensor (pressure, altitude, temperature, humidity). 

## PI 3B Pinout with BCM chip numbering: https://pinout.xyz/

## BME280 (weather sensors) and RTC hookup guide:

- These both use I2C and will need to be wired in parallel to the 
same two Pi pins. Break out the SDA and SCL pins of the Pi (either 
via PCB or simply wires to a breadboard).

- Both the BME280 and RTC boards have the SDA and SCL lines labeled, 
simply connect them both to each respective node on the 
breadboard/PCB. 

- Use power pins on Pi as necessary.

## Tamarisk 320 hookup: 

- Attach yellow VGA cable to usb video card. 

- **Power via alternate power source to avoid overcurrent draw from the 
Pi.**
 
- Dataline to the Pi is the USB end of the video card

## Pure thermal: Simply connect via USB.

**CAMERA NOTE:** Currently the code only snaps a picture with one 
camera. Tamarisk 320 saves a black screen when attempting to also capture a 
single frame from it, this might be to due a mismatch with the RGB 
argument given.

## USAGE: 

- Simply run main.py and as long as everything is hooked up it 
will take a picture with the FIRST camera that was connected and 
save a txt file with the datalogged info from the weather sensors. 
It will create a new directory based on a constant you can set in 
main.py, and timestamps both the directory and each newly created 
file via their names.

## FFMPEG NOTES:

- The way the tiffs are created is by giving FFMPEG's 
-compression_algo the argument "raw" or "0" (fully uncompressed) 
then having it capture 1 frame via the -vframes argument.

- The input device is chosen using "-i $DEVICE". Linux will mount USB 
video devices in the /dev/video# directories in order from when 
they were mounted (e.g the first device will be video0, second 
video1, etc). 

**EXAMPLE:** sudo ffmpeg -i /dev/video0 -compression_algo raw -vframes 
1 $filename

- When running this for the Tamarisk 320 there is an issue mapping 
RGB values to a picture, and the uncompressed argument will produce 
a fully black image. 

**TODO:** Multithreading implementation to run both cameras simultaneously. 

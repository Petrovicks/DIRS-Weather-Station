import time
import board
import busio
import adafruit_bme280

def bme280_init(pressure):
    # Initialize i2c object via the busio import.
    i2c = busio.I2C(board.SCL, board.SDA)

    # Initialize bme280 object via adafruit library.
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

    # Hardcoded calibration of sensor to current location's sea level pressure (hPa)
    bme280.sea_level_pressure = pressure

    # Returns object to be used to read out sensor data.
    return bme280

def main():
    print("Using 1013.25 hPa as location's default sea level pressure.")
    bme280 = bme280_init(1013.25)
    print("\nTemperature: %0.1f C" % bme280.temperature)
    print("Humidity: %0.1f %%" % bme280.humidity)
    print("Pressure: %0.1f hPa" % bme280.pressure)
    print("Altitude = %0.2f meters" % bme280.altitude)

if __name__ == '__main__':
    print("Running BME280 example..")
    try:
        main()
    except Exception as e:
        raise TypeError(e)
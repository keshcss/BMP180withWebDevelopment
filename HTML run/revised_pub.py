from __future__ import division 
import time
import mraa
import paho.mqtt.client as mqtt
import sqlite3


mqttBroker = "192.168.1.173"
client = mqtt.Client("Temp")
client.connect(mqttBroker)

"""Codes"""
# BMP085 default address.
BMP085_I2CADDR           = 0x77

# Operating Modes
BMP085_ULTRALOWPOWER     = 0
BMP085_STANDARD          = 1
BMP085_HIGHRES           = 2
BMP085_ULTRAHIGHRES      = 3

# BMP085 Registers
BMP085_CAL_AC1           = 0xAA  # R   Calibration data (16 bits)
BMP085_CAL_AC2           = 0xAC  # R   Calibration data (16 bits)
BMP085_CAL_AC3           = 0xAE  # R   Calibration data (16 bits)
BMP085_CAL_AC4           = 0xB0  # R   Calibration data (16 bits)
BMP085_CAL_AC5           = 0xB2  # R   Calibration data (16 bits)
BMP085_CAL_AC6           = 0xB4  # R   Calibration data (16 bits)
BMP085_CAL_B1            = 0xB6  # R   Calibration data (16 bits)
BMP085_CAL_B2            = 0xB8  # R   Calibration data (16 bits)
BMP085_CAL_MB            = 0xBA  # R   Calibration data (16 bits)
BMP085_CAL_MC            = 0xBC  # R   Calibration data (16 bits)
BMP085_CAL_MD            = 0xBE  # R   Calibration data (16 bits)
BMP085_CONTROL           = 0xF4
BMP085_TEMPDATA          = 0xF6
BMP085_PRESSUREDATA      = 0xF6

# Commands
BMP085_READTEMPCMD       = 0x2E
BMP085_READPRESSURECMD   = 0x34


class BMP085(object):
    def __init__(self, mode=BMP085_STANDARD, address=BMP085_I2CADDR, i2c=None, **kwargs):
        self._mode = mode
        self.UT = 0

        # Create I2C device.
        if i2c is None:
            i2c = mraa.I2c(0)
            i2c.address(0x77)
            
        self._device = i2c
        # Load calibration values.
        #self._load_calibration()
        self._load_datasheet_calibration()

    def _load_calibration(self):
        self.cal_AC1 = self._device.readWordReg(BMP085_CAL_AC1)   # INT16
        self.cal_AC2 = self._device.readWordReg(BMP085_CAL_AC2)   # INT16
        self.cal_AC3 = self._device.readWordReg(BMP085_CAL_AC3)   # INT16
        self.cal_AC4 = self._device.readWordReg(BMP085_CAL_AC4)   # UINT16
        self.cal_AC5 = self._device.readWordReg(BMP085_CAL_AC5)   # UINT16
        self.cal_AC6 = self._device.readWordReg(BMP085_CAL_AC6)   # UINT16
        self.cal_B1 = self._device.readWordReg(BMP085_CAL_B1)     # INT16
        self.cal_B2 = self._device.readWordReg(BMP085_CAL_B2)     # INT16
        self.cal_MB = self._device.readWordReg(BMP085_CAL_MB)     # INT16
        self.cal_MC = self._device.readWordReg(BMP085_CAL_MC)     # INT16
        self.cal_MD = self._device.readWordReg(BMP085_CAL_MD)     # INT16

    def _load_datasheet_calibration(self):
        # Set calibration from values in the datasheet example.  Useful for debugging the
        # temp and pressure calculation accuracy.
        self.cal_AC1 = 408
        self.cal_AC2 = -72
        self.cal_AC3 = -14383
        self.cal_AC4 = 32741
        self.cal_AC5 = 32757
        self.cal_AC6 = 23153
        self.cal_B1 = 6190
        self.cal_B2 = 4
        self.cal_MB = -32767
        self.cal_MC = -8711
        self.cal_MD = 2868

    def read_raw_temp(self):
        """Reads the raw (uncompensated) temperature from the sensor."""
        self._device.writeWordReg(BMP085_CONTROL, BMP085_READTEMPCMD)
        time.sleep(0.005)
        msb1 = self._device.readReg(BMP085_TEMPDATA)
        lsb1 = self._device.readReg(BMP085_TEMPDATA+1)
        raw = ((msb1 << 8) + lsb1)
        return raw

    def read_raw_pressure(self):
        """Reads the raw (uncompensated) pressure level from the sensor."""
        self._device.writeWordReg(BMP085_CONTROL, BMP085_READPRESSURECMD + (self._mode << 6))
        time.sleep(0.005)
        msb = self._device.readReg(BMP085_PRESSUREDATA)
        lsb = self._device.readReg(BMP085_PRESSUREDATA+1)
        xlsb = self._device.readReg(BMP085_PRESSUREDATA+2)
        raw = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self._mode)
        #self._logger.debug('Raw pressure 0x{0:04X} ({1})'.format(raw & 0xFFFF, raw))
        return raw

    def read_temperature(self):
        """Gets the compensated temperature in degrees celsius."""
        self.UT = self.read_raw_temp()
        # Datasheet value for debugging:
        #UT = 27898
        # Calculations below are taken straight from section 3.5 of the datasheet.
        X1 = ((self.UT - self.cal_AC6) * self.cal_AC5) >> 15
        X2 = (self.cal_MC << 11) // (X1 + self.cal_MD)
        B5 = X1 + X2
        temp = ((B5 + 8) >> 4) / 10.0
        return temp
        

    def read_pressure(self):
        """Gets the compensated pressure in Pascals."""
        #UT = self.read_raw_temp()
        UP = self.read_raw_pressure()
        # Datasheet values for debugging:
        #UT = 27898
        #UP = 23843
        # Calculations below are taken straight from section 3.5 of the datasheet.
        # Calculate true temperature coefficient B5.
        X1 = ((self.UT - self.cal_AC6) * self.cal_AC5) >> 15
        X2 = (self.cal_MC << 11) // (X1 + self.cal_MD)
        B5 = X1 + X2
        # Pressure Calculations
        B6 = B5 - 4000
        X1 = (self.cal_B2 * (B6 * B6) >> 12) >> 11
        X2 = (self.cal_AC2 * B6) >> 11
        X3 = X1 + X2
        B3 = (((self.cal_AC1 * 4 + X3) << self._mode) + 2) // 4
        X1 = (self.cal_AC3 * B6) >> 13
        X2 = (self.cal_B1 * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self.cal_AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> self._mode)
        if B7 < 0x80000000:
            p = (B7 * 2) // B4
        else:
            p = (B7 // B4) * 2
        X1 = (p >> 8) * (p >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * p) >> 16
        p = p + ((X1 + X2 + 3791) >> 4)
        return p/1000

    def read_altitude(self, sealevel_pa=101325.0):
        """Calculates the altitude in meters."""
        # Calculation taken straight from section 3.6 of the datasheet.
        pressure = float(self.read_pressure())
        altitude = 44330.0 * (1.0 - pow(pressure / sealevel_pa, (1.0/5.255)))
        return altitude

    def read_sealevel_pressure(self, altitude_m=0.0):
        """Calculates the pressure at sealevel when given a known altitude in
        meters. Returns a value in Pascals."""
        pressure = float(self.read_pressure())
        p0 = pressure / pow(1.0 - altitude_m/44330.0, 5.255)
        return p0
    
#declare

bmp085 = BMP085()
count = 1
device = "ID: 7688(1)"
#shortforms
n = "Reading: "
dc = " Degree Celcuis"
kp = " kPa"
nl = " "
#m = " Metres\n"
bmp085_temperature = 0
bmp085_pressure = 0

while True:
    client.publish("Reading", str(count)+ " : " +device)
    print("\nReading: " + str(count))
    bmp085_temperature = bmp085.read_temperature()
    client.publish("Temperature", str(bmp085_temperature) + dc)
    print("Published Temperature: " + str(bmp085_temperature) + " to Temperature")
    bmp085_pressure = bmp085.read_pressure()
    client.publish("Pressure", str(bmp085_pressure) + kp)
    print("Published Pressure: " + str(bmp085_pressure) + " to Pressure") 
    client.publish("newl", nl)
    count = count + 1
    time.sleep(2.5)

import logging
import smbus2
import time
import math


class PWM(object):
    FREQUENCY = 60
    BUS_NUMBER = 1
    I2C_ADDRESS = 0x40

    MODE1 = 0x00
    MODE2 = 0x01
    SUBADR1 = 0x02
    SUBADR2 = 0x03
    SUBADR3 = 0x04
    PRESCALE = 0xFE
    LED0_ON_L = 0x06
    LED0_ON_H = 0x07
    LED0_OFF_L = 0x08
    LED0_OFF_H = 0x09
    ALL_LED_ON_L = 0xFA
    ALL_LED_ON_H = 0xFB
    ALL_LED_OFF_L = 0xFC
    ALL_LED_OFF_H = 0xFD

    RESTART = 0x80
    SLEEP = 0x10
    ALLCALL = 0x01
    INVRT = 0x10
    OUTDRV = 0x04

    def __init__(self) -> None:
        self.bus = smbus2.SMBus(self.BUS_NUMBER)

    def setup(self) -> None:
        """Init the class with busNumber and address"""
        logging.info('[PWM] Resetting PCA9685 MODE1 (without SLEEP) and MODE2')
        self.writeAllValue(0, 0)
        self.writeByteData(self.MODE2, self.OUTDRV)
        self.writeByteData(self.MODE1, self.ALLCALL)
        time.sleep(0.005)

        mode1 = self.readByteData(self.MODE1)
        mode1 = mode1 & ~self.SLEEP
        self.writeByteData(self.MODE1, mode1)
        time.sleep(0.005)

        self.frequency = self.FREQUENCY

    def writeByteData(self, reg, value) -> None:
        """Write data to I2C with self.I2C_ADDRESS"""
        logging.info('[PWM] Writing value %2X to %2X', value, reg)
        try:
            self.bus.write_byte_data(self.I2C_ADDRESS, reg, value)
        except Exception as i:
            print(i)
            self.check_i2c()

    def readByteData(self, reg):
        """Read data from I2C with self.I2C_ADDRESS"""
        logging.info('[PWM] Reading value from %2X' % reg)
        try:
            results = self.bus.read_byte_data(self.I2C_ADDRESS, reg)
            return results
        except Exception as i:
            print(i)
            self.check_i2c()

    def runCommand(self, cmd):
        import subprocess
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = p.stdout.read().decode('utf-8')
        status = p.poll()
        print(result)
        print(status)
        return status, result

    def check_i2c(self):
        from os import listdir
        print("I2C bus number is: %s" % self.BUS_NUMBER)
        print("Checking I2C device:")
        devices = listdir("/dev/")
        if "i2c-%d" % self.BUS_NUMBER in devices:
            print("I2C device exist.")
        else:
            print("Seems like I2C have not been set, run 'sudo raspi-config' to enable I2C")
        cmd = "i2cdetect -y %s" % self.BUS_NUMBER
        _, output = self.runCommand(cmd)
        print("Your PCA9685 address is set to 0x%02X" % self.I2C_ADDRESS)
        print("i2cdetect output:")
        print(output)
        outputs = output.split('\n')[1:]
        addresses = []
        for tmpAddresses in outputs:
            tmpAddresses = tmpAddresses.split(':')
            if len(tmpAddresses) < 2:
                continue
            else:
                tmpAddresses = tmpAddresses[1]
            tmpAddresses = tmpAddresses.strip().split(' ')
            for address in tmpAddresses:
                if address != '--':
                    addresses.append(address)
        print("Connected i2c device:")
        if addresses == []:
            print("None")
        else:
            for address in addresses:
                print("  0x%s" % address)
        if "%02X" % self.I2C_ADDRESS in addresses:
            print("Wierd, I2C device is connected, Try to run the program again")
        else:
            print("Device is missing.")
            print("Check the address or wiring of PCA9685 Server driver")
            quit()

    @property
    def frequency(self) -> int:
        return self.FREQUENCY

    @frequency.setter
    def frequency(self, freq: int) -> None:
        """Set PWM frequency"""
        logging.info('[PWM] Set frequency to %d', freq)
        preScaleValue = 25000000.0
        preScaleValue /= 4096.0
        preScaleValue /= float(freq)
        preScaleValue -= 1.0
        logging.info('[PWM] Setting PWM frequency to %d Hz', freq)
        logging.info('[PWM] Estimated pre-scale: %d', preScaleValue)
        preScale = math.floor(preScaleValue + 0.5)
        logging.info('[PWM] Final pre-scale: %d', preScale)

        oldMode = self.readByteData(self.MODE1)
        newMode = (oldMode & 0x7F) | 0x10
        self.writeByteData(self.MODE1, newMode)
        self.writeByteData(self.PRESCALE, int(math.floor(preScale)))
        self.writeByteData(self.MODE1, oldMode)
        time.sleep(0.005)
        self.writeByteData(self.MODE1, oldMode | 0x80)

    def write(self, channel, on, off) -> None:
        """Set on and off value on specific channel"""
        logging.info('[PWM] Set channel "%d" to value "%d"', channel, off)
        self.writeByteData(self.LED0_ON_L + 4 * channel, on & 0xFF)
        self.writeByteData(self.LED0_ON_H + 4 * channel, on >> 8)
        self.writeByteData(self.LED0_OFF_L + 4 * channel, off & 0xFF)
        self.writeByteData(self.LED0_OFF_H + 4 * channel, off >> 8)

    def writeAllValue(self, on, off) -> None:
        """Set on and off value on all channel"""
        logging.info('[PWM] Set all channel to value "%d"', off)
        self.writeByteData(self.ALL_LED_ON_L, on & 0xFF)
        self.writeByteData(self.ALL_LED_ON_H, on >> 8)
        self.writeByteData(self.ALL_LED_OFF_L, off & 0xFF)
        self.writeByteData(self.ALL_LED_OFF_H, off >> 8)

    def map(self, x, in_min, in_max, out_min, out_max):
        """To map the value from arange to another"""
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

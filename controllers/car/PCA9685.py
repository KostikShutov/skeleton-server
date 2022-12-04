import logging
import smbus2
import time


class PWM(object):
    _MODE1 = 0x00
    _MODE2 = 0x01
    _SUBADR1 = 0x02
    _SUBADR2 = 0x03
    _SUBADR3 = 0x04
    _PRESCALE = 0xFE
    _LED0_ON_L = 0x06
    _LED0_ON_H = 0x07
    _LED0_OFF_L = 0x08
    _LED0_OFF_H = 0x09
    _ALL_LED_ON_L = 0xFA
    _ALL_LED_ON_H = 0xFB
    _ALL_LED_OFF_L = 0xFC
    _ALL_LED_OFF_H = 0xFD

    _RESTART = 0x80
    _SLEEP = 0x10
    _ALLCALL = 0x01
    _INVRT = 0x10
    _OUTDRV = 0x04

    def __init__(self,
                 busNumber: int,
                 address: int) -> None:
        self.busNumber = busNumber
        self.address = address

        self.bus = smbus2.SMBus(self.busNumber)

    def setup(self) -> None:
        """Init the class with busNumber and address"""
        logging.info('[PWM] Reseting PCA9685 MODE1 (without SLEEP) and MODE2')
        self.writeAllValue(0, 0)
        self.writeByteData(self._MODE2, self._OUTDRV)
        self.writeByteData(self._MODE1, self._ALLCALL)
        time.sleep(0.005)

        mode1 = self.readByteData(self._MODE1)
        mode1 = mode1 & ~self._SLEEP
        self.writeByteData(self._MODE1, mode1)
        time.sleep(0.005)

    def writeByteData(self, reg, value) -> None:
        """Write data to I2C with self.address"""
        logging.info('[PWM] Writing value %2X to %2X', value, reg)
        try:
            self.bus.write_byte_data(self.address, reg, value)
        except Exception as i:
            print(i)
            self.check_i2c()

    def readByteData(self, reg):
        """Read data from I2C with self.address"""
        logging.info('[PWM] Reading value from %2X' % reg)
        try:
            results = self.bus.read_byte_data(self.address, reg)
            return results
        except Exception as i:
            print(i)
            self.check_i2c()

    def runCommand(self, cmd):
        import subprocess
        p = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = p.stdout.read().decode('utf-8')
        status = p.poll()
        # print(result)
        # print(status)
        return status, result

    def check_i2c(self):
        from os import listdir
        print("I2C bus number is: %s" % self.busNumber)
        print("Checking I2C device:")
        devices = listdir("/dev/")
        if "i2c-%d" % self.busNumber in devices:
            print("I2C device exist.")
        else:
            print("Seems like I2C have not been set, run 'sudo raspi-config' to enable I2C")
        cmd = "i2cdetect -y %s" % self.busNumber
        _, output = self.runCommand(cmd)
        print("Your PCA9685 address is set to 0x%02X" % self.address)
        print("i2cdetect output:")
        print(output)
        outputs = output.split('\n')[1:]
        addresses = []
        for tmp_addresses in outputs:
            tmp_addresses = tmp_addresses.split(':')
            if len(tmp_addresses) < 2:
                continue
            else:
                tmp_addresses = tmp_addresses[1]
            tmp_addresses = tmp_addresses.strip().split(' ')
            for address in tmp_addresses:
                if address != '--':
                    addresses.append(address)
        print("Connected i2c device:")
        if addresses == []:
            print("None")
        else:
            for address in addresses:
                print("  0x%s" % address)
        if "%02X" % self.address in addresses:
            print(
                "Wierd, I2C device is connected, Try to run the program again, If problem stills, email this information to support@sunfounder.com")
        else:
            print("Device is missing.")
            print(
                "Check the address or wiring of PCA9685 Server driver, or email this information to support@sunfounder.com")
            quit()

    def write(self, channel, on, off) -> None:
        """Set on and off value on specific channel"""
        logging.info('[PWM] Set channel "%d" to value "%d"', channel, off)
        self.writeByteData(self._LED0_ON_L + 4 * channel, on & 0xFF)
        self.writeByteData(self._LED0_ON_H + 4 * channel, on >> 8)
        self.writeByteData(self._LED0_OFF_L + 4 * channel, off & 0xFF)
        self.writeByteData(self._LED0_OFF_H + 4 * channel, off >> 8)

    def writeAllValue(self, on, off) -> None:
        """Set on and off value on all channel"""
        logging.info('[PWM] Set all channel to value "%d"', off)
        self.writeByteData(self._ALL_LED_ON_L, on & 0xFF)
        self.writeByteData(self._ALL_LED_ON_H, on >> 8)
        self.writeByteData(self._ALL_LED_OFF_L, off & 0xFF)
        self.writeByteData(self._ALL_LED_OFF_H, off >> 8)

    def map(self, x, in_min, in_max, out_min, out_max):
        """To map the value from arange to another"""
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

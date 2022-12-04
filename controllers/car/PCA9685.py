import logging
import smbus2
import time
import math


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

    def __init__(self, busNumber: int = 1, address: int = 0x40) -> None:
        self.busNumber = busNumber
        self.address = address

        self.bus = smbus2.SMBus(self.busNumber)

    def setup(self) -> None:
        """Init the class with busNumber and address"""
        logging.info('[PWM] Reseting PCA9685 MODE1 (without SLEEP) and MODE2')
        self.write_all_value(0, 0)
        self._write_byte_data(self._MODE2, self._OUTDRV)
        self._write_byte_data(self._MODE1, self._ALLCALL)
        time.sleep(0.005)

        mode1 = self._read_byte_data(self._MODE1)
        mode1 = mode1 & ~self._SLEEP
        self._write_byte_data(self._MODE1, mode1)
        time.sleep(0.005)
        self._frequency = 60

    def _write_byte_data(self, reg, value) -> None:
        """Write data to I2C with self.address"""
        logging.info('[PWM] Writing value %2X to %2X', value, reg)
        try:
            self.bus.write_byte_data(self.address, reg, value)
        except Exception as i:
            print(i)
            self._check_i2c()

    def _read_byte_data(self, reg):
        """Read data from I2C with self.address"""
        logging.info('[PWM] Reading value from %2X' % reg)
        try:
            results = self.bus.read_byte_data(self.address, reg)
            return results
        except Exception as i:
            print(i)
            self._check_i2c()

    def _run_command(self, cmd):
        import subprocess
        p = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = p.stdout.read().decode('utf-8')
        status = p.poll()
        # print(result)
        # print(status)
        return status, result

    def _check_i2c(self):
        from os import listdir
        print("I2C bus number is: %s" % self.busNumber)
        print("Checking I2C device:")
        devices = listdir("/dev/")
        if "i2c-%d" % self.busNumber in devices:
            print("I2C device exist.")
        else:
            print("Seems like I2C have not been set, run 'sudo raspi-config' to enable I2C")
        cmd = "i2cdetect -y %s" % self.busNumber
        _, output = self._run_command(cmd)
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

    @property
    def frequency(self) -> int:
        return self._frequency

    @frequency.setter
    def frequency(self, freq) -> None:
        """Set PWM frequency"""
        logging.info('[PWM] Set frequency to %d', freq)
        self._frequency = freq
        prescale_value = 25000000.0
        prescale_value /= 4096.0
        prescale_value /= float(freq)
        prescale_value -= 1.0
        logging.info('[PWM] Setting PWM frequency to %d Hz', freq)
        logging.info('[PWM] Estimated pre-scale: %d', prescale_value)
        prescale = math.floor(prescale_value + 0.5)
        logging.info('[PWM] Final pre-scale: %d', prescale)

        old_mode = self._read_byte_data(self._MODE1);
        new_mode = (old_mode & 0x7F) | 0x10
        self._write_byte_data(self._MODE1, new_mode)
        self._write_byte_data(self._PRESCALE, int(math.floor(prescale)))
        self._write_byte_data(self._MODE1, old_mode)
        time.sleep(0.005)
        self._write_byte_data(self._MODE1, old_mode | 0x80)

    def write(self, channel, on, off) -> None:
        """Set on and off value on specific channel"""
        logging.info('[PWM] Set channel "%d" to value "%d"', channel, off)
        self._write_byte_data(self._LED0_ON_L + 4 * channel, on & 0xFF)
        self._write_byte_data(self._LED0_ON_H + 4 * channel, on >> 8)
        self._write_byte_data(self._LED0_OFF_L + 4 * channel, off & 0xFF)
        self._write_byte_data(self._LED0_OFF_H + 4 * channel, off >> 8)

    def write_all_value(self, on, off) -> None:
        """Set on and off value on all channel"""
        logging.info('[PWM] Set all channel to value "%d"', off)
        self._write_byte_data(self._ALL_LED_ON_L, on & 0xFF)
        self._write_byte_data(self._ALL_LED_ON_H, on >> 8)
        self._write_byte_data(self._ALL_LED_OFF_L, off & 0xFF)
        self._write_byte_data(self._ALL_LED_OFF_H, off >> 8)

    def map(self, x, in_min, in_max, out_min, out_max):
        """To map the value from arange to another"""
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

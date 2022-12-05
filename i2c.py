#!/usr/bin/python

import time
import os

RPI_REVISION_0 = ['900092']
RPI_REVISION_1 = ['0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '000d', '000e', '000f', '0010',
                  '0011', '0012', '0013']
RPI_REVISION_2 = ['a01041', 'a21041']
RPI_REVISION_3 = ['a02082', 'a22082']
RPI_REVISION_4 = ['a03111', 'b03111', 'b03112', 'b03114', 'c03111', 'c03112', 'c03114', 'd03114']


def getCpuNumber() -> str:
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line.startswith('Revision'):
                return line[11:-1]
    except Exception as e:
        print('Open file error:', e)
        return 'Open file error'


def getRevision(cpuNumber: str):
    if cpuNumber in RPI_REVISION_0:
        return 0
    elif cpuNumber in RPI_REVISION_1:
        return 1
    elif cpuNumber in RPI_REVISION_2:
        return 2
    elif cpuNumber in RPI_REVISION_3:
        return 3
    elif cpuNumber in RPI_REVISION_4:
        return 4
    else:
        return cpuNumber


def getBusNumber(cpuNumber: int) -> int:
    revision = getRevision(cpuNumber)
    if revision in [2, 3, 4]:
        return 1
    elif revision in [0, 1]:
        return 0
    else:
        raise ValueError('Error occur while getting Pi Revision. Revision: %s' % revision)


def removeLine(tfile: str, sstr: str) -> None:
    i2c_list = []
    try:
        lines = open(tfile, 'r').readlines()
        flen = len(lines) - 1
        for i in range(flen):
            if sstr in lines[i]:
                i2c_list.append(i)
        for i in range(len(i2c_list) - 1, 0, -1):
            lines.remove(lines[i2c_list[i]])
        open(tfile, 'w').writelines(lines)
    except Exception as e:
        print('Remove line:', e)


def addLine(tfile: str, sstr: str) -> None:
    try:
        lines = open(tfile, 'r').readlines()
        lines.append(sstr)
        open(tfile, 'w').writelines(lines)
    except Exception as e:
        print('Add line:', e)


def modifyConfig() -> None:
    removeLine('/boot/config.txt', 'dtparam=i2c_arm=')
    addLine('/boot/config.txt', '\ndtparam=i2c_arm=on\n')


if __name__ == '__main__':
    print('')
    print('====================================')
    print('||                                ||')
    print('||     Raspberry Pi I2C check     ||')
    print('||                                ||')
    print('====================================')
    print('')
    time.sleep(1)
    print("Checking your Pi's information.")
    time.sleep(1)
    cpuNumber = getCpuNumber()
    print('Your cpu revision: %s' % cpuNumber)
    time.sleep(1)
    print('Your Raspberry Pi is Revision: %s' % getRevision(cpuNumber))
    time.sleep(1)
    busNumber = getBusNumber(cpuNumber)
    print('Your I2C bus number is: %s' % busNumber)
    time.sleep(1)
    print('')
    time.sleep(1)
    print('Checking your device...')
    isFine = False
    device = 'i2c-' + str(busNumber)
    for dev in os.listdir('/dev/'):
        if dev == device:
            isFine = True
    time.sleep(1)
    if isFine:
        print('I2C setting is fine.')
        time.sleep(1)
        print('Runing i2cdetect.')
        time.sleep(1)
        print('')
        command = 'i2cdetect -y ' + str(busNumber)
        os.system(command)
    else:
        print('I2C has not been setup.')
        time.sleep(1)
        print('')
        time.sleep(1)
        print('Backup...')
        os.system('cp /boot/config.txt /boot/config.bak')
        print('Done')
        time.sleep(1)
        print('Setting i2c...')
        modifyConfig()
        print('Done')
        time.sleep(1)
        print('I2C has set. It would change after reboot.')
        time.sleep(1)
        check = input('Do you want to reboot now? (y/n)')
        flag = True
        while flag:
            if check in ['y', 'Y']:
                print('Your Raspberry Pi will be reboot in 5 second.')
                for i in range(6):
                    time.sleep(1)
                    print('', 5 - i)
                print('Rebooting...')
                flag = False
                os.system('reboot')
            elif check in ['n', 'N']:
                time.sleep(1)
                print('Done.')
                flag = False
            else:
                print('It should be "Y" or "N", in capital or not. Try again.')

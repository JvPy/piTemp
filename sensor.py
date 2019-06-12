import os
import glob
import time
from datetime import datetime, date

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder0 = glob.glob(base_dir + '28*')[0]
device_folder1 = glob.glob(base_dir + '28*')[1]
#s3 = glob.glob(base_dir + '28*')[0]
device_file0 = device_folder0 + '/w1_slave'
device_file1 = device_folder1 + '/w1_slave'
#device_file0 = device_folder0 + '/w1_slave'

def read_temp_raw(sensorNumber):
    f = open(eval(sensorNumber), 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(sensorNumber):
    lines = read_temp_raw(sensorNumber)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return str(temp_c)

while True:
    for sensorNumber in range(2):
        sensor = "device_file"+str(sensorNumber)
        tempRead = read_temp(sensor)
        print("[*] Sensor " + str(sensorNumber) + " :"  + tempRead + " C")
        f = open("temp.csv", "a")
        f.write(str(sensorNumber) + ";" + str(datetime.now()) + ";" + tempRead+"\n")
        f.close()

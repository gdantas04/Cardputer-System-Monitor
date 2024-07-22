import psutil, serial, time
import serial.tools.list_ports

def cpu_sender():
    cpu_to_send = [str(psutil.cpu_percent(1)),
               str(int(psutil.cpu_freq().current)),
               str(int(psutil.sensors_temperatures()['coretemp'][1][1]))]    # You should change this according to your CPU name
    
    return cpu_to_send


def disk_sender():
    disks = []
    for tupla in psutil.disk_partitions():
        disks.append(tupla[0])

    disk_to_send = [str(psutil.disk_usage('/')[3]),
               str(disks),
               str(int(psutil.sensors_temperatures()['nvme'][1][1]))]    # You should change this according to your disk

    return disk_to_send


def other_sender():
    other_to_send = [str(int(psutil.sensors_battery()[0])),
                     str(int(psutil.sensors_battery()[1]/60)),
                     str(psutil.virtual_memory().percent)]

    return other_to_send



portas = serial.tools.list_ports.comports()
print('\n---- CARDPUTER SERIAL SENDER ----\n\nChoose the port number:')

k = 0
ports_dict = {}

for porta in portas:
    print(f"{k}:    {porta.device}")
    ports_dict[k] = porta.device
    k+=1

result = int(input('\n> '))

result = ports_dict[int(result)]


ser = serial.Serial(result, 9600)
time.sleep(2) # time to establish serial connection

print(f'\nSending serial data to port {result}')


while(True):
    to_send = ['0','newcicle','trash'] + cpu_sender() + disk_sender() + other_sender()
    for info in to_send:
        ser.write((info + '\n').encode())

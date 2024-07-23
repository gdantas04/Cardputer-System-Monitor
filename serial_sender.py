import json, psutil, serial, time, serial.tools.list_ports


if psutil.sensors_temperatures() == {}:
    state = False
else:
    state = True


if psutil.sensors_battery() == None:
    state_bat = False
else:
    state_bat = True


with open('user_settings.json') as f:
    settings = json.load(f)


def cpu_sender(arg1):

    if state == False:
        cpu_to_send = [str(psutil.cpu_percent(1)),str(int(psutil.cpu_freq().current)),"-"]
    else:
        cpu_to_send = [str(psutil.cpu_percent(1)),str(int(psutil.cpu_freq().current)),str(int(psutil.sensors_temperatures()[arg1][1][1]))]
    
    return cpu_to_send


def disk_sender(arg2):
    disks = []
    for tupla in psutil.disk_partitions():
        disks.append(tupla[0]) 


    if state == False:
        disk_to_send = [str(psutil.disk_usage('/')[3]),str(disks),"-"]
    else:
        disk_to_send = [str(psutil.disk_usage('/')[3]),str(disks),str(int(psutil.sensors_temperatures()[arg2][1][1]))]

    return disk_to_send


def other_sender():

    if state_bat == False:
        other_to_send = ["-","-",str(psutil.virtual_memory().percent)]
    else:
        other_to_send = [str(int(psutil.sensors_battery()[0])),str(int(psutil.sensors_battery()[1]/60)),str(psutil.virtual_memory().percent)]

    return other_to_send


def setup_config():

    if settings == {"cpu_temp_sensor":0,"disk_temp_sensor":0}:
        c = 0
        j = 0 
        cpu_dict = {}
        disk_dict = {}

        temp_sensors = list(psutil.sensors_temperatures().keys())


        print("Looks like it's your first time running this program, let's configure your profile.\n\nI'm gonna list your temperature sensors.\n\nSelect the one who is related to your CPU temperature:")
        for elem in temp_sensors:
            print(f'[{c}] {elem}')
            cpu_dict[c] = elem
            c+=1
        cpu_sensor = int(input('\n> '))
        cpu_sensor = cpu_dict[cpu_sensor]

        temp_sensors.remove(cpu_sensor)


        print("\nRight! Now choose the one who is related to your Disk temperature:")
        for elem in temp_sensors:
            print(f'[{j}] {elem}')
            disk_dict[j] = elem
            j+=1
        disk_sensor = int(input('\n> '))
        disk_sensor = disk_dict[disk_sensor]

        settings["cpu_temp_sensor"] = cpu_sensor
        settings["disk_temp_sensor"] = disk_sensor

        with open('user_settings.json', 'w') as f:
            json.dump(settings, f)



print('\n---- CARDPUTER SERIAL SENDER ----\n\n')

if state == True:
    setup_config()

portas = serial.tools.list_ports.comports()
print('Choose the port number:')

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
    to_send = ['0','newcicle','trash'] + cpu_sender(settings["cpu_temp_sensor"]) + disk_sender(settings["disk_temp_sensor"]) + other_sender()
    for info in to_send:
        ser.write((info + '\n').encode())

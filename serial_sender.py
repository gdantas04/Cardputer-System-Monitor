# https://github.com/gdantas04/Cardputer-System-Monitor



import json, psutil, serial, time, serial.tools.list_ports, os



# To manage interface

class Interface:
    def __init__(self):
        self.columns = os.get_terminal_size().columns
        self.lines = os.get_terminal_size().lines

    def drawTitle(self, character, text):
        print(character*self.columns + "\n" + f"{character*2}{text: ^{self.columns-4}}{character*2}" + "\n" + character*self.columns)
    
    def clearScreenExceptTitle(self, character, text):
        os.system('clear')
        print(character*self.columns + "\n" + f"{character*2}{text: ^{self.columns-4}}{character*2}" + "\n" + character*self.columns)
    
    def clearScreen(self):
        os.system('clear')



# To loag json config file

with open('user_settings.json') as f:
    settings = json.load(f)



# To see if there are temperature sensors available

if psutil.sensors_temperatures() == {}:
    state = False
else:
    state = True



# To see if there are bettery sensors available

if psutil.sensors_battery() == None:
    state_bat = False
else:
    state_bat = True



# To see if configuration has already been done

if settings == {"cpu_temp_sensor":0,"disk_temp_sensor":0}:
    settings_state = False
else:
    settings_state = True



# Function to process cpu information

def cpu_sender(arg1):

    if state == False:
        cpu_to_send = [str(psutil.cpu_percent(1)),str(int(psutil.cpu_freq().current)),"-"]
    else:
        cpu_to_send = [str(psutil.cpu_percent(1)),str(int(psutil.cpu_freq().current)),str(int(psutil.sensors_temperatures()[arg1][0][1]))]
    
    return cpu_to_send



# Function to process disks information

def disk_sender(arg2):
    disks = []
    for tupla in psutil.disk_partitions():
        disks.append(tupla[0]) 

    if state == False:
        disk_to_send = [str(psutil.disk_usage('/')[3]),str(disks),"-"]
    else:
        disk_to_send = [str(psutil.disk_usage('/')[3]),str(disks),str(int(psutil.sensors_temperatures()[arg2][0][1]))]

    return disk_to_send



# Function to process other informations

def other_sender():

    if state_bat == False:
        other_to_send = ["-","-",str(psutil.virtual_memory().percent)]
    else:
        other_to_send = [str(int(psutil.sensors_battery()[0])),str(int(psutil.sensors_battery()[1]/60)),str(psutil.virtual_memory().percent)]

    return other_to_send



# Function to config user settings

def setup_config():
    temp_sensors = []

    print("\nLooks like it's your first time running this program, let's configure your profile.\n\nI'm gonna list your temperature sensors.\n\nSelect the one who is related to your CPU temperature:")
    
    for temp_sensor in list(psutil.sensors_temperatures().keys()):
        print(f'[{list(psutil.sensors_temperatures().keys()).index(temp_sensor)}] {temp_sensor}')
        temp_sensors.append(temp_sensor)

    cpu_sensor = temp_sensors[int(input('\n> '))]

    temp_sensors.remove(cpu_sensor)

    interface.clearScreenExceptTitle('#', 'Cardputer System Monitor')

    print("\nRight! Now choose the one who is related to your Disk temperature:")


    for temp_sensor in temp_sensors:
        print(f'[{list(psutil.sensors_temperatures().keys()).index(temp_sensor)}] {temp_sensor}')

    disk_sensor = temp_sensors[int(input('\n> '))]

    interface.clearScreenExceptTitle('#', 'Cardputer System Monitor')

    settings["cpu_temp_sensor"], settings["disk_temp_sensor"] = cpu_sensor, disk_sensor

    with open('user_settings.json', 'w') as f:
        json.dump(settings, f)



interface = Interface()



# To see if user have to configure something
interface.clearScreen()
interface.drawTitle('#', 'Cardputer System Monitor')

if (settings_state == False) and (state == True):
    setup_config()



# To choose the port to establish connection

print('\nChoose the port number:')

portas = []
for porta in serial.tools.list_ports.comports():
    print(f"{serial.tools.list_ports.comports().index(porta)}:    {porta.device}")
    portas.append(porta.device)
 
result = portas[int(input('\n> '))]



# Start serial connection

ser = serial.Serial(result, 9600)
time.sleep(2) 



# Send data

interface.clearScreenExceptTitle('#', 'Cardputer System Monitor')

print(f'\nSending serial data to port {result}')
while(True):
    to_send = ['0','newcicle','trash'] + cpu_sender(settings["cpu_temp_sensor"]) + disk_sender(settings["disk_temp_sensor"]) + other_sender()
    for info in to_send:
        ser.write((info + '\n').encode())

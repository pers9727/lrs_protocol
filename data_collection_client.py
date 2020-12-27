import netifaces

ifaces = netifaces.interfaces()
type_txt = '/home/pi/lrs_protocol/type.txt'
cpu_info = '/proc/cpuinfo'
command_txt = '/home/pi/lrs_protocol/commands.txt'

all = []
ifaces_data = []
type_data = []
commands_data = []

"""
Add information about type-module
"""

with open(type_txt, 'r') as file:
    module_type_data = file.read()

"""
 Add information about commands and number of commands
"""

number_of_commands = 0
commands_info = open(command_txt)
for lines in commands_info:
    number_of_commands += 1
    commands_data.append(lines)


"""
 Add information about raspberry 
"""

cpu_info_data = []
cpu_info = open(cpu_info)
for lines in cpu_info:
    if ('Hardware' in lines) or ('Revision' in lines) or ('Serial' in lines) or ('Model' in lines):
        cpu_info_data.append(lines)

""" 
  Compile on one data
"""

all.append(module_type_data)
all.append(str(number_of_commands) + " commands in module")
all.append(commands_data)
all.append(str(len(ifaces)) + ' active interfaces')
all.append(ifaces)
all.append(cpu_info_data)

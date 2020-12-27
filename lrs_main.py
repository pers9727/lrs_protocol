import os
import time
import work_with_files
import logging

logger = logging.getLogger(__name__)

"""
    Module's types:
        L - claw
        V - vehicle platform (car, tank)
        C - camera
        F - flying platform (copter)
        D - dog, like as boston dynamics
        S - scientific instruments
        
"""


"""
    Programs:
       0 - 2DVC - Two diodes and a camera on the top
       1 - SDC - Self-driving car
       2 - SBC - Stream camera in browser
       3 - DPR - Define people at room
       4 - VCL - Vehicle claw camera
       
"""

"""
    Program's type module:
        If program's type without '+', use one module. For example:
            VC - One module required (If module is absent, use several modules)
        If with '+' use several modules. 
"""


ssh_directory = '/home/pi/projects/'
commands_file = '/home/roman/lrs_protocol/commands.txt'
ip_type_file = '/home/roman/lrs_protocol/ip_type.txt'


def main_func():
    problem_with_program = []
    execute_programs = []

    while True:
        action = input("[ACT] What action do you want?\n"
                       "0 - Reboot some module/s\n"
                       "1 - Start program\n")

        if action == '0':
            print('[ACT] Choose modules, which you want to reboot')
            mod_reb = map(int, input().split())
            for i in list(mod_reb):
                os.system(f' ssh pi@10.42.43.{i} \'sudo reboot\'')

        else:
            if len(problem_with_program) != 0:
                print(f'[LOG] You have not completed programm {problem_with_program}')
            time.sleep(1)
            answer = input('[ACT] Do you want to start program? (y/n)\n')
            if answer == 'y':
                com_data = work_with_files.read(commands_file)
                for com in range(len(com_data)):
                    com_data[com] = com_data[com].split('_')

                while True:
                    command_number = int(input(f'[ACT] Enter commands number ({0} to {len(com_data) - 1}):'
                                               f'\n{com_data})\n'))

                    if 0 <= command_number < len(com_data):
                        print(f'[ACT] Choosing program № {command_number} {com_data[command_number]}\n')
                        time.sleep(1)

                        print(f'[LOG] For this program you need {(com_data[command_number][1]).count("+") + 1} '
                              f'module/s\n')
                        serv_com = com_data[command_number][1]
                        time.sleep(1)

                        print('[LOG] Searching modules for this program\n')

                        ip_type_data = work_with_files.read(ip_type_file)
                        for modules in range(len(ip_type_data)):
                            ip_type_data[modules] = ip_type_data[modules].split('_')
                        if '+' in serv_com:
                            serv_com = serv_com.split('+')
                        else:
                            x = serv_com
                            serv_com = []
                            serv_com.append(x)

                        ip = []
                        time.sleep(1)
                        for z in serv_com:
                            for y in ip_type_data:
                                if z in y[1] and (y[0] not in ip):
                                    ip.append(y[0])
                                    print(f'[ACT] Choosing module with ip: {y[0]} as module {z}\n')
                                    break
                        time.sleep(1)
                        if len(ip) > 0:
                            print(f'[LOG] Start {com_data[command_number]}\n')
                        else:
                            print('[LOG] No modules for your program. Start program with single modules?\n')

                        for i in ip:
                            os.system(f'[LOG] ssh pi@{i} \'python3 {ssh_directory}{com_data[command_number][3]}\'')
                        if logger:
                            print('[LOG] Program is not completed!!!')

                            problem_with_program.append(com_data[command_number][0])
                        break
                    else:
                        print('[LOG] Incorrect input, please repeat')
                        continue

            elif answer == 'n':
                print('[LOG] Exit from protocol')
                break
            else:
                print('[LOG] Bad variant, please repeat')
            time.sleep(1)


if __name__ == '__main__':
    main_func()

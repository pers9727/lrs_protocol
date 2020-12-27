import os
dirName = '/home/roman/lrs_protocol/module_information'
names = os.listdir(dirName)
for name in names:
    fullname = os.path.join(dirName, name) # получаем полное имя
    if os.path.isfile(fullname):
        print(fullname[-6:])
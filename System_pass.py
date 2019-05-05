#! python3.7
# Архивирует файлы и складывает их по дате
# данные берет из path_file.py файла с данными

import datetime, os, shutil, zipfile  # mport modules
import path_list

#path_backup = "d:\\programm\\python\\projects\\automatic\\backup\\1"
#path_file = "d:\\programm\\python\\projects\\automatic\\backup"
path_file = path_list.path_file # file with path to backup


def notest_file(text):
    """Create and write logs in file"""
    with open("info_file.txt", "a", encoding="utf-8", ) as f:
        f.write(text)


def get_date(format_of_date):
    """function get current time in nidded format"""
    current_date = datetime.datetime.today().strftime(format_of_date)  # "%d%m%Y"
    return current_date


notest_file("start: " + get_date("%d%m%Y_%H:%S") + "\n")
print("start: " + get_date("%d%m%Y_%H:%S"))
current_pass = os.getcwd()

try:
    os.chdir(path_file)
except:
    print("не правильный путь файла")
    notest_file("не правильный путь файла")

exemple_zip = zipfile.ZipFile((get_date("%d%m%Y") + ".zip"), "w")
exemple_zip.write("test.txt", compress_type=zipfile.ZIP_DEFLATED)

# exemple_info = exemple_zip.getinfo("test.txt") # get info from file
# print(exemple_info.compress_size) # out size information

exemple_zip.close()

os.chdir(current_pass)
notest_file("end: " + get_date("%d%m%Y") + "\n")
print("end: " + get_date("%d%m%Y_%H:%S"))

# # os.makedirs("d:\\programm\\python\\projects\\automatic\\backup")
# print(os.getcwd())
# print(os.path.getatime("d:\\programm\\python\\projects\\automatic"))
# print(os.listdir("d:\\programm\\python\\projects\\automatic\\backup"))
# shutil.move("d:\\programm\\python\\projects\\automatic\\test.txt", "d:\\programm\\python\\projects\\automatic\\backup")
# os.chdir("d:\\programm\\python\\projects\\automatic\\backup")
# exemple_zip = zipfile.ZipFile("new.zip", "w")
# exemple_zip.write("test.txt", compress_type=zipfile.ZIP_DEFLATED)
# exemple_zip.close()
# # TODO: разобраться как архивировать папку

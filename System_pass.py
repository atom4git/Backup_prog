#! python3.7
# Архивирует файлы и складывает их по дате
# данные берет из path_file.py файла с данными

import datetime, os, shutil, zipfile  # mport modules
import path_list

path_file = path_list.path_file  # path to backup
arch_obj = path_list.arch_obj  # folder or file to backup
debug = path_list.debug  # debug level


def notest_file(text):
    """Create and write logs in file"""
    if debug == 2:
        print(text)
        with open("info_file.txt", "a", encoding="utf-8", ) as f:
            f.write(text + "\n")
    elif debug == 1:
        with open("info_file.txt", "a", encoding="utf-8", ) as f:
            f.write(text + "\n")


def get_date(format_of_date):
    """function get current time in nidded format"""
    current_date = datetime.datetime.today().strftime(format_of_date)  # "%d%m%Y"
    return current_date


def zip_file(arch_obj):
    """create zip file end incert information in it"""
    with zipfile.ZipFile(get_date("%d%m%Y") + '.zip', 'w') as myzip:
        myzip.write(arch_obj)
    pass


def test_path():
    """
    verify file or directory availability. If file or directory does not exist:
    :return: close program
    """
    testpath = path_file + arch_obj
    notest_file(testpath)

    if os.path.exists(testpath):
        if os.path.isfile(testpath):
            notest_file('ФАЙЛ')
            notest_file('Размер:' + str(os.path.getsize(testpath) // 1024) + 'Кб')
            notest_file('Дата создания:' + str(datetime.datetime.fromtimestamp(int(os.path.getctime(testpath)))))
            notest_file(
                'Дата последнего открытия:' + str(datetime.datetime.fromtimestamp(int(os.path.getatime(testpath)))))
            notest_file(
                'Дата последнего изменения:' + str(datetime.datetime.fromtimestamp(int(os.path.getmtime(testpath)))))
        elif os.path.isdir(testpath):
            notest_file('КАТАЛОГ')
            notest_file('Список объектов в нем: ', os.listdir(testpath))
    else:
        notest_file("object not found")
        os.abort()


notest_file("start: " + get_date("%d%m%Y_%H:%S"))
current_pass = os.getcwd()

test_path()
os.chdir(path_file)
zip_file(arch_obj)
os.chdir(current_pass)
notest_file("end: " + get_date("%d%m%Y") + "\n" + "=" * 10 + "\n")


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

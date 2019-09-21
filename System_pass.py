#! python3.7
# Архивирует файлы и складывает их по дате
# данные берет из path_file.py файла с данными

import datetime, os, ftplib  # import modules shutil
import path_list

path_to_file = path_list.path_to_file  # path to backup
arch_obj = path_list.arch_obj  # folder or file to backup
debug = path_list.debug  # debug level
backup_objects = path_list.path_to_backup


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

    # 1. Файлы и каталоги, которые необходимо скопировать, собираются в список.
    source = backup_objects
    # Заметьте, что для имён, содержащих пробелы, необходимо использовать
    # двойные кавычки внутри строки.
    # 2. Резервные копии должны храниться в основном каталоге резерва.
    if not os.path.exists(path_to_file + "\\backup"):
        os.makedirs(path_to_file + "\\backup")
    target_dir = "d:\\programm\\python\\projects\\backup_prog\\backup\\backup"  # Подставьте тот путь, который вы будете использовать.
    # 3. Файлы помещаются в zip-архив.
    # 4. Именем для zip-архива служит текущая дата и время.
    name_of_zip_file = (get_date("%d%m%Y_%H.%S") + '.zip')
    target = target_dir + os.sep + name_of_zip_file
    # print(target)
    # 5. Используем команду "zip" для помещения файлов в zip-архив
    zip_command = "zip -qr {0} {1}".format(target, ' '.join(source))
    # Запускаем создание резервной копии
    if os.system(zip_command) == 0:
        notest_file('Suchesful' + target)
    else:
        notest_file('Somthing wrong with arhiving')
    return name_of_zip_file


def test_path():
    """
    verify file or directory availability. If file or directory does not exist:
    :return: close program
    """
    testpath = path_to_file + arch_obj
    notest_file(testpath)  # action log

    if os.path.exists(testpath):
        if os.path.isfile(testpath):
            notest_file('File')  # action log
            notest_file('Size:' + str(os.path.getsize(testpath) // 1024) + 'Kb')  # action log
            notest_file(
                'Criate date:' + str(datetime.datetime.fromtimestamp(int(os.path.getctime(testpath)))))  # action log
            notest_file(
                'Date last open:' + str(datetime.datetime.fromtimestamp(int(os.path.getatime(testpath)))))  # action log
            notest_file(
                'Date last change:' + str(
                    datetime.datetime.fromtimestamp(int(os.path.getmtime(testpath)))))  # action log
        elif os.path.isdir(testpath):
            notest_file('Direcrory')  # action log
            notest_file('Files in Dir: ' + str(os.listdir(testpath)))  # action log
    else:
        notest_file("object not found")  # action log
        os.abort()


def copy_to_ftp(path):
    # login data
    host = path_list.ip_server  # get server's IP from config file
    ftp_user = path_list.server_log  # get user's Login from config file
    ftp_password = path_list.server_pass  # get user's Password from config file

    ftp = ftplib.FTP(host)
    notest_file(ftp.login(ftp_user, ftp_password))  # action log
    ftp.cwd('home/backup')
    notest_file(ftp.getwelcome())  # action log

    # list_dir = os.listdir()
    # print(ftp.nlst())
    os.chdir(path_to_backup)
    # print(os.getcwd())
    list_dir = os.listdir()

    for i in list_dir:
        # print(i)
        ftp.storbinary("STOR " + i, open(i, "rb"), 1024)

    ftp.quit()


os.chdir(path_to_file)
notest_file("start: " + get_date("%d%m%Y_%H:%S"))

test_path()
os.chdir(path_to_file)

name_of_zip_file = zip_file(arch_obj)
notest_file(name_of_zip_file)  # action log
path_to_backup = path_to_file + "\\backup\\"
copy_to_ftp(path_to_backup)
os.chdir(path_to_file)
notest_file("end: " + get_date("%d%m%Y_%H:%S") + "\n" + "=" * 10 + "\n")  # action log

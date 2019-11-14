#! python3.7
# Архивирует файлы и складывает их по дате
# данные берет из path_file.py файла с данными

import datetime, os, ftplib, zipfile, hashlib  # import modules
import path_list  # list with settings

# import settings
path_to_file = path_list.path_to_file  # path to backup
arch_obj = path_list.arch_obj  # folder or file to backup
debug = path_list.debug  # debug level
backup_objects = path_list.path_to_backup
path_for_backup = path_list.path_for_backup
folder_on_server = path_list.folder_on_server

home_dir = os.getcwd()  # gets the script directory


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


def zip_file(backup_objects):
    """create zip file end incert information in it"""

    # Get name from date_time
    name_of_zip_file = (get_date("%d%m%Y_%H.%S") + '.zip')
    # put files in zip archiv
    z = zipfile.ZipFile(name_of_zip_file, 'a', zipfile.ZIP_DEFLATED)  # create archive
    for i in backup_objects:
        if os.path.isdir(i):
            for root, dirs, files in os.walk(i):  # get list of files in folder
                for file in files:
                    z.write(os.path.join(root, file))  # Создание относительных путей и запись файлов в архив
        else:
            z.write(i)
    z.close()
    if zipfile.is_zipfile(name_of_zip_file):
        notest_file("arckhiving is conplite! Created file" + name_of_zip_file)
    return name_of_zip_file


# def test_path():
#     """
#     verify file or directory availability. If file or directory does not exist:
#     :return: close program
#     """
#     testpath = (i, for i in backup_objects)
#     notest_file(testpath)  # action log
#
#     if os.path.exists(testpath):
#         if os.path.isfile(testpath):
#             notest_file('File')  # action log
#             notest_file('Size:' + str(os.path.getsize(testpath) // 1024) + 'Kb')  # action log
#             notest_file(
#                 'Criate date:' + str(datetime.datetime.fromtimestamp(int(os.path.getctime(testpath)))))  # action log
#             notest_file(
#                 'Date last open:' + str(datetime.datetime.fromtimestamp(int(os.path.getatime(testpath)))))  # action log
#             notest_file(
#                 'Date last change:' + str(
#                     datetime.datetime.fromtimestamp(int(os.path.getmtime(testpath)))))  # action log
#         elif os.path.isdir(testpath):
#             notest_file('Direcrory')  # action log
#             notest_file('Files in Dir: ' + str(os.listdir(testpath)))  # action log
#     else:
#         notest_file("object not found")  # action log
#         os.abort()


def copy_to_ftp(path):
    """copy oll files on user's FTP"""

    # login data
    os.chdir(home_dir)
    host = path_list.ip_server  # get server's IP from config file
    ftp_user = path_list.server_log  # get user's Login from config file
    ftp_password = path_list.server_pass  # get user's Password from config file

    ftp = ftplib.FTP(host)
    notest_file(ftp.login(ftp_user, ftp_password))  # action log ,"5000"
    # ftp.set_pasv(True)
    # ftp.pwd()
    ftp.cwd(folder_on_server)
    notest_file(ftp.getwelcome())  # action log
    os.chdir(path_for_backup)
    list_dir = os.listdir()


    for i in list_dir:
        # print(i)
        ftp.storbinary("STOR " + i, open(i, "rb"), 1024)
    ftp.quit()

if not os.path.exists(path_for_backup):
    os.makedirs(path_for_backup)
# os.chdir(path_to_file)
notest_file("start: " + get_date("%d%m%Y_%H:%S"))


name_of_zip_file = zip_file(backup_objects)
os.rename((os.getcwd() + "\\" + name_of_zip_file), (path_for_backup + "\\" + name_of_zip_file))
copy_to_ftp(name_of_zip_file)
os.remove(name_of_zip_file)
os.chdir(home_dir)
notest_file("end: " + get_date("%d%m%Y_%H:%S") + "\n" + "=" * 10 + "\n")  # action log


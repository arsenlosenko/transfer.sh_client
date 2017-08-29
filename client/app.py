#!/usr/bin/env python3

"""
Script that uploads files in entered directory as an archive to transfer.sh, for easy downloading.
"""

import os
import sys
import zipfile
import requests
import datetime
import pyperclip


def create_zip():
    if len(sys.argv) > 1:
        path_to_folder = sys.argv[1]
    else:
        path_to_folder = input("Please enter directory: \n")

    if os.path.isdir(path_to_folder):
        os.chdir(path_to_folder)
        zip_name = 'files_archive_{}.zip'.format(str(datetime.datetime.now())[5:16].replace(' ', "_"))
        files = os.listdir()
        print("Creating zipfile from files in...", path_to_folder)
        with zipfile.ZipFile(zip_name, 'w') as zip:
            for img in files:
                zip.write(img)
                print("Added file: ", img)

        return zip_name
    else:
        print("Please enter a valid absolute path to directory")
        sys.exit()


def send_zip():
    zip_file = create_zip()
    size_of_file = get_archive_size(zip_file)
    final_date = get_date_in_two_weeks()

    print("\nSending zipfile: {} (size of the file: {} MB)".format(zip_file, size_of_file))
    url = 'https://transfer.sh/'
    file = {'file': open(zip_file, 'rb')}
    response = requests.post(url, files=file)
    download_link = response.content.decode('utf-8')
    print("Link to download zipfile(will be saved till {}):\n{}".format(final_date, download_link))

    try:
        pyperclip.copy(download_link)
    except:
        print("There is no copy/paste environment, please install one of the following packages:\n"
              "sudo apt-get install\n" 
              "sudo apt-get install xclip")
    print("Link copied to clipboard")
    confirm_removal(zip_file)


def get_date_in_two_weeks():
    today = datetime.datetime.today()
    date_in_two_weeks = today + datetime.timedelta(days=14)
    return date_in_two_weeks.date()


def get_archive_size(file):
    size_in_bytes = os.path.getsize(file)
    size_in_megabytes = size_in_bytes / 1000000
    return size_in_megabytes


def confirm_removal(zip_file):
    confirmation = input('\nDelete files in the directory?(y/n, Y/N, archive): ')
    if (confirmation == 'y') or (confirmation == 'Y'):
        clean_up()
    elif (confirmation == 'n') or (confirmation == 'N'):
        print("OK, files will be there")
        sys.exit()
    elif confirmation == 'archive':
        remove_archive(zip_file)
    else:
        print("Please enter a valid answer (y/n, Y/N)")
        confirm_removal()


def remove_archive(file_name):
    print("Deleting archive: ", file_name)
    os.remove(file_name)
    print("File removed")


def clean_up():
    print('\nCleaning up...')
    files = os.listdir()
    for f in files:
        os.remove(f)
        print("Removed file: ", f)


def print_help():
    print("Usage:\n transfer_files /path/to/files - archive directly"
          "\n transfer_files - start script with prompt "
          "\n transfer_files -h - print help message")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        print_help()
    else:
        try:
            send_zip()
        except KeyboardInterrupt:
            print("\nExecution stopped")


if __name__ == '__main__':
    main()

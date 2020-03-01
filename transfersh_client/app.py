#!/usr/bin/env python3

"""
author: Arsen Losenko
email: arsenlosenko@gmail.com
github: arsenlosenko
short description: command-line tool that uploads files to transfer.sh and returns download link
"""

import os
import sys
import zipfile
import requests
import datetime
import pyperclip
import argparse


def get_date_in_two_weeks():
    """
    get maximum date of storage for file
    :return: date in two weeks
    """
    today = datetime.datetime.today()
    date_in_two_weeks = today + datetime.timedelta(days=14)
    return date_in_two_weeks.date()


def get_size(file):
    """
    get file size, in megabytes
    :param file:
    :return: size of file
    """
    size_in_bytes = os.path.getsize(file)
    size_in_megabytes = size_in_bytes / 1000000
    return size_in_megabytes


def parse_params():
    usage = "%prog [-i/--file/--directory] /path/to/file [--rm-archive/--rm-file]\n" \
            "Short description:\n" \
            "transfersh-client is used to send files to transfer.sh and retrieve download link, " \
            "so it could be shared fast and easily directly from command-line.\n" \
            "It can send all files from entered directory (in an archive) or send one file.\n" \
            "You can download up to 10 GB files to transfer.sh, they will be saved there for 14 days."
    parser = argparse.ArgumentParser(usage)
    parser.add_argument('-i', '--interactive',
                      dest="interactive_mode",
                      action="store_true",
                      help="run in interactive mode (with entering info in the prompt)")
    parser.add_argument('-d', '--directory',
                      dest="directory",
                      action="store",
                      help="enter absolute path to directory, and create archive of it")
    parser.add_argument('-f', '--file',
                      dest="file",
                      action="store",
                      help="path to file which will be uploaded")
    parser.add_argument("-s", "--send",
                        dest="send",
                        action="store",
                        help="path to file or directory that will be sent to transfer.sh (can be used instead of -f or-d)")
    parser.add_argument('--rf', '--rm-file',
                      dest="rm_file",
                      action="store_true",
                      help="remove files after sending")
    parser.add_argument('--ra', '--rm-archive',
                      dest="rm_arch",
                      action="store_true",
                      help="remove only created archive")
    args = parser.parse_args()

    return args, parser


def check_params():
    """
    check if entered params are in correct usage (and prevent incorrect usage)
    :return: options in correct form
    """
    args, parser = parse_params()

    if args.interactive_mode:
        print("During interactive mode all other options are omitted")
    elif args.send:
        print("Using file provided by --send option, omitting --file and --directory")
    elif (args.file and args.rm_arch) \
            or (args.directory and args.rm_file):
        print("Use either --ra or --rf accordingly:\n")
        parser.print_help()
        sys.exit()
    elif (args.file and args.directory) \
            or (args.rm_arch and args.rm_file):
        print("Use either -f or -d options\n")
        parser.print_help()
        sys.exit()
    else:
        return args

def handle_params():
    """
    Function retrieves options from check_params() and runs functions accordingly to their state
    (which flags were used)
    :return: None
    """
    args = check_params()
    if args.interactive_mode or len(sys.argv) == 1:
        run_interactive_mode()

    filename = args.file
    directory = args.directory

    if filename is not None:
        try:
            os.path.isfile(filename)
        except FileNotFoundError:
            print("Please enter valid absolute path to file")
            sys.exit()
        else:
            filename = check_absolute_path(filename)
            if args.rm_file:
                send_to_transfersh(filename)
                remove_file(filename)
            else:
                send_to_transfersh(filename)

    directory = args.directory
    if directory is not None:
        try:
            os.path.isdir(directory)
        except NotADirectoryError:
            print("Please enter valid absolute path to directory")
            sys.exit()
        else:
            directory = check_absolute_path(directory)
            if args.rm_arch:
                zip_file = create_zip(directory)
                send_to_transfersh(zip_file)
                remove_file(zip_file)
            else:
                zip_file = create_zip(directory)
                send_to_transfersh(zip_file)

def check_absolute_path(path):
    """
    check if entered directory is absolute, if not, format it to absolute
    :param path: path that was entered by user
    :return: absolute path
    """
    if os.path.isabs(path) is False:
        path = os.path.join(os.getcwd(), path)
    return path


def run_interactive_mode():
    """
    running mode which asks user's data via prompt
    :return: None
    """
    path = input("Enter path to file or directory:\n")
    path = check_absolute_path(path)

    if os.path.isfile(path):
        send_to_transfersh(path)
        confirm = input("Remove file? (y/n, yes/no):")
        confirm_removal(confirm, path)
    elif os.path.isdir(path):
        zip_file = create_zip(path)
        send_to_transfersh(zip_file)
        confirm = input("Remove archive? (y/n, yes/no):")
        confirm_removal(confirm, zip_file)
    else:
        print("Please enter a valid absolute path to file/directory")
        sys.exit()


def create_zip(file_dir):
    """
    create zipfile from files in entered directory
    :param file_dir: absolute path to directory
    :return: absolute path to created zipfile
    """
    os.chdir(file_dir)
    zip_name = 'files_archive_{}.zip'.format(str(datetime.datetime.now())[5:16].replace(' ', "_"))
    files = os.listdir()
    print("Creating zipfile from files in...", file_dir)
    with zipfile.ZipFile(zip_name, 'w') as zip:
        for f in files:
            zip.write(f)
            print("Added file: ", f)

    zip_path = file_dir + "/" + zip_name

    # double check if path is absolute
    if os.path.isabs(zip_path):
        return zip_path
    else:
        return os.getcwd() + "/" + zip_name


def remove_file(file):
    print("Removing file...", file)
    os.remove(file)
    print("Removed.")


def confirm_removal(confirm, filename):
    """
    function used in interactive mode, asks weather to remove file, or not
    :param confirm:
    :param filename: absolute path to file
    :return: None
    """
    if confirm == 'y' or confirm == 'yes':
        remove_file(filename)
    elif confirm == 'n' or confirm == 'no':
        print("File will stay there")
    else:
        print("Please etner a valid answer (y/n, yes/no)")
        confirm_removal()


def send_to_transfersh(file):
    """
    send file to transfersh, retrieve download link, and copy it to clipboard
    :param file: absolute path to file
    :return: None
    """
    size_of_file = get_size(file)
    final_date = get_date_in_two_weeks()
    file_name = os.path.basename(file)

    print("\nSending file: {} (size of the file: {} MB)".format(file_name, size_of_file))
    url = 'https://transfer.sh/'
    file = {'{}'.format(file): open(file, 'rb')}
    response = requests.post(url, files=file)
    download_link = response.content.decode('utf-8')
    print("Link to download file(will be saved till {}):\n{}".format(final_date, download_link))

    copy_to_clipboard(download_link)


def copy_to_clipboard(link):
    """
    copy dowload link to clipboard
    :param link: dowload link for file
    :return: None
    """
    try:
        pyperclip.copy(link)
    except:
        print("There is no copy/paste environment, please install one of the following packages:\n"
              "sudo apt-get update\n"
              "sudo apt-get install xclip")
    print("Link copied to clipboard")


def main():
    try:
        handle_params()
    except KeyboardInterrupt:
        print('Execution stopped')
        sys.exit()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

"""
author: Arsen Losenko
email: arsenlosenko@protonmail.com
github: arsenlosenko
short description: command-line tool that uploads files to transfer.sh and returns download link
"""

import os
import sys
import zipfile
import requests
import datetime
import pyperclip
import optparse
import wget


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
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--interactive',
                      dest="interactive_mode",
                      action="store_true",
                      help="run in interactive mode (with entering info in the prompt)")
    parser.add_option('-d', '--directory',
                      dest="directory",
                      action="store",
                      type="string",
                      help="enter absolute path to directory, and create archive of it")
    parser.add_option('-f', '--file',
                      dest="file",
                      action="store",
                      type="string",
                      help="absolute path to file which will be uploaded")
    parser.add_option('--rf', '--rm-file',
                      dest="rm_file",
                      action="store_true",
                      help="remove files after sending")
    parser.add_option('--ra', '--rm-archive',
                      dest="rm_arch",
                      action="store_true",
                      help="remove only created archive")
    (options, args) = parser.parse_args()

    return options, args, parser


def check_params():
    """
    check if entered params are in correct usage (and prevent incorrect usage)
    :return: options in correct form
    """
    params = parse_params()
    options = params[0]
    parser = params[2]

    # handle incorrect usage of options (a bit of spaghetti code)
    if (options.interactive_mode and options.file) \
            or (options.interactive_mode and options.directory) \
            or (options.interactive_mode and options.rm_arch) \
            or (options.interactive_mode and options.rm_file):
        print("Interactive option is used separately from other options\n")
        parser.print_help()
        sys.exit()
    elif (options.file and options.rm_arch) \
            or (options.directory and options.rm_file):
        print("Use either --ra or --rf accordingly:\n")
        parser.print_help()
        sys.exit()
    elif (options.file and options.directory) \
            or (options.rm_arch and options.rm_file):
        print("Use either -f or -d options\n")
        parser.print_help()
        sys.exit()
    else:
        return options


def check_absolute_path(path):
    """
    check if entered directory is absolute, if not, format it to absolute
    :param path: path that was entered by user
    :return: absolute path
    """
    current_dir = os.getcwd()
    if os.path.isabs(path) is False:
        if str(path).startswith("./"):
            return current_dir + path[1:]
        else:
            return current_dir + "/" + path
    else:
        return path


def handle_params():
    """
    Function retrieves options from check_params() and runs functions accordingly to their state
    (which flags were used)
    :return: None
    """
    options = check_params()
    if options.interactive_mode or len(sys.argv) == 1:
        interactive_mode_run()

    # check if file or directory exists, and weather to remove created archive or file
    if options.file is not None:
        try:
            os.path.isfile(options.file)
        except FileNotFoundError:
            print("Please enter valid absolute path to file")
            sys.exit()
        else:
            options.file = check_absolute_path(options.file)
            if options.rm_file:
                send_to_transfersh(options.file)
                remove_file(options.file)
            else:
                send_to_transfersh(options.file)

    if options.directory is not None:
        try:
            os.path.isdir(options.directory)
        except NotADirectoryError:
            print("Please enter valid absolute path to directory")
            sys.exit()
        else:
            options.directory = check_absolute_path(options.directory)
            if options.rm_arch:
                zip_file = create_zip(options.directory)
                send_to_transfersh(zip_file)
                remove_file(zip_file)
            else:
                zip_file = create_zip(options.directory)
                send_to_transfersh(zip_file)


def interactive_mode_run():
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
        create_zip(path)
        send_to_transfersh(path)
        confirm = input("Remove archive? (y/n, yes/no):")
        confirm_removal(confirm, path)
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


def send_to_transfersh(file, clipboard=True):
    """
    send file to transfersh, retrieve download link, and copy it to clipboard
    :param file: absolute path to file
    :param copy_to_clipboard: boolean value specifing if the download_link should be copied to clipboard
    :return: download_link
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

    if clipboard:
        copy_to_clipboard(download_link)
    return download_link


def download_from_transfersh(download_link, path='.'):
    """
    download file from transfersh
    :param download_link: link to uploaded file
    :param path:  directory or file path for file to be downloaded
    :return: path where the file is downloaded
    """
    return wget.download(download_link,out=path)


def copy_to_clipboard(link):
    """
    copy dowload link to clipboard
    :param link: dowload link for file
    :return: None
    """
    pyperclip.copy(link)
    print("Link copied to clipboard")


def main():
    try:
        handle_params()
    except KeyboardInterrupt:
        print('Execution stopped')
        sys.exit()


if __name__ == '__main__':
    main()

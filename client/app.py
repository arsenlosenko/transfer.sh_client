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
import optparse


# TODO: overall refactor (namely send_file and send_zip)


def get_date_in_two_weeks():
    today = datetime.datetime.today()
    date_in_two_weeks = today + datetime.timedelta(days=14)
    return date_in_two_weeks.date()


def get_size(file):
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


def handle_params():
    options = check_params()

    # convert entered directory or file to its absolute path
    if options.file is not None and os.path.isabs(options.file) is False:
        current_dir = os.getcwd()
        if str(options.file).startswith("./"):
            options.file = current_dir + options.file[1:]
        else:
            options.file = current_dir + "/" + options.file

    if options.directory is not None and os.path.isabs(options.directory) is False:
        current_dir = os.getcwd()
        if str(options.directory).startswith("./"):
            options.directory = current_dir + options.directory[1:]
        else:
            options.directory = current_dir + "/" + options.directory

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
            if options.rm_file:
                file_path = send_file(options.file)
                remove_file(file_path)
            else:
                send_file(options.file)

    if options.directory is not None:
        try:
            os.path.isdir(options.directory)
        except NotADirectoryError:
            print("Please enter valid absolute path to directory")
            sys.exit()
        else:
            if options.rm_arch:
                zipfile = send_zip(options.directory)
                remove_file(zipfile)
            else:
                send_zip(options.directory)


def interactive_mode_run():
    path = input("Enter path to file or directory:\n ")
    if os.path.isabs(path) is False:
        if path.startswith('./'):
            abs_path = os.getcwd() + path[1:]
        else:
            abs_path = os.getcwd() + "/" + path

    if os.path.isfile(abs_path):
        send_file(abs_path)
        confirm = input("Remove file? (y/n, yes/no):")
        confirm_removal(confirm, abs_path)
    elif os.path.isdir(abs_path):
        arch_name = send_zip(abs_path)
        confirm = input("Remove archive? (y/n, yes/no):")
        confirm_removal(confirm, arch_name)
    else:
        print("Please enter a valid absolute path to file/directory")
        sys.exit()


def create_zip(file_dir):
    os.chdir(file_dir)
    zip_name = 'files_archive_{}.zip'.format(str(datetime.datetime.now())[5:16].replace(' ', "_"))
    files = os.listdir()
    print("Creating zipfile from files in...", file_dir)
    with zipfile.ZipFile(zip_name, 'w') as zip:
        for img in files:
            zip.write(img)
            print("Added file: ", img)

    return zip_name


def remove_file(file):
    print("Removing file...", file)
    os.remove(file)
    print("Removed.")


def confirm_removal(confirm, filename):
    if confirm == 'y' or confirm == 'yes':
        remove_file(filename)
    elif confirm == 'n' or confirm == 'no':
        print("File will stay there")
    else:
        print("Please etner a valid answer (y/n, yes/no)")
        confirm_removal()


def send_zip(file_dir):
    zip_file = create_zip(file_dir)
    size_of_file = get_size(zip_file)
    final_date = get_date_in_two_weeks()

    print("\nSending zipfile: {} (size of the file: {} MB)".format(zip_file, size_of_file))
    url = 'https://transfer.sh/'
    file = {'{}'.format(zip_file): open(zip_file, 'rb')}
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

    # convert to absolute path (just for double check)
    abs_path_to_archive = os.getcwd() + "/" + zip_file
    return abs_path_to_archive


def send_file(file_path):
    size_of_file = get_size(file_path)
    final_date = get_date_in_two_weeks()
    filename_from_path = os.path.basename(file_path)

    print("\nSending file: {} (size of the file: {} MB)".format(file_path, size_of_file))
    url = 'https://transfer.sh/'
    file = {'{}'.format(filename_from_path): open(filename_from_path, 'rb')}
    response = requests.post(url, files=file)
    download_link = response.content.decode('utf-8')
    print("Link to download file(will be saved till {}):\n{}".format(final_date, download_link))

    try:
        pyperclip.copy(download_link)
    except:
        print("There is no copy/paste environment, please install one of the following packages:\n"
              "sudo apt-get install\n"
              "sudo apt-get install xclip")
    print("Link copied to clipboard")
    return file_path


def main():
    try:
        handle_params()
    except KeyboardInterrupt:
        print('Execution stopped')
        sys.exit()


if __name__ == '__main__':
    main()
# transfer.sh-client
Python client for uploading files to transfer.sh (https://transfer.sh/)
This command-line tool send file (or files, in case of directory download) to transfer.sh, and provides link to uploaded files,
so it could be easily shared

# Latest release:

https://pypi.python.org/pypi/transfersh-client/1.0.7

# Getting Started
- Install python and pip (package manager):
~~~~
sudo apt-get update

sudo apt-get install python3 python3-pip

OR

sudo apt-get install python python-pip
~~~~
- Download package from pip:
~~~
sudo pip3 install transfersh_client

OR

sudo pip install trnasfersh_client
~~~

# Usage

- After installation, you can run this package directly in command line. Launching it without arguments starts it in interactive mode:
~~~
transfer_files
~~~

### Sample output:
~~~~
Github|⇒ transfer_files
Enter path to file or directory: ./sysinfo
Creating zipfile from files in... /home/path/to/directory/sysinfo
Added file:  cython_tut.cpython-34m.so
Added file:  cython_tut.pyx
Added file:  setup.py
Added file:  build
Added file:  fib.cpython-34m.so
Added file:  primes.c
Added file:  .idea
Added file:  fib.c
Added file:  parse_proc_files.py
Added file:  fib.pyx
Added file:  primes.pyx
Added file:  cython_tut.c
Added file:  primes.cpython-34m.so

Sending zipfile: files_archive_09-02_18:34.zip (size of the file: 0.407897 MB)
Link to download zipfile(will be saved till 2017-09-16):
Could not save metadata

Link copied to clipboard
Remove archive? (y/n, yes/no):yes
Removing file... /home/path/to/directory/sysinfo/files_archive_09-02_18:34.zip
Removed.
~~~~
- Besides that, you can start it with arguments:

   -i --interactive - keys that will start app with prompts (same as running it without arguments)

   -d --directory - enter path to directory (relative or absolute), which files will be sent in an archive

   -f --file - same as --directory, but enter path to file

   --ra --rm-archive - delete created archive, after it was sent

   --rf --rm-file - delete file after it was sent

   -h --help - display help message

### Sample output
~~~
transfer.sh_client|dev⚡ ⇒ transfer_files -f test.txt --rf

Sending file: /home/path/to/directory/transfer.sh_client/test.txt (size of the file: 0.000113 MB)
Link to download file(will be saved till 2017-09-16):
https://transfer.sh/CtaJs/test.txt
Link copied to clipboard
Removing file... /home/path/to/directory/transfer.sh_client/test.txt
Removed.

~~~

## Example of usage inside scripts 

~~~
#!/usr/bin/env python3

from transfersh_client.app import send_to_transfersh, create_zip, remove_file


def send_files_from_dir():
    directory = './'
    zip_file = create_zip(directory)  # creates zip archive and returns it's absolute path
    send_to_transfersh(zip_file)  # sends archive to transfer.sh
    remove_file(zip_file)  # removes it


if __name__ == '__main__':
    send_files_from_dir()

~~~


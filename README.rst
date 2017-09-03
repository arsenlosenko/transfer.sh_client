============
Usage:
============


- After installation, you can run this package directly in command line. Launching it without arguments starts it in interactive mode:

================
Sample output:
================
::

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



- Besides that, you can start it with arguments:

   -i --interactive - keys that will start app with prompts (same as running it without arguments)

   -d --directory - enter path to directory (relative or absolute), which files will be sent in an archive

   -f --file - same as --directory, but enter path to file

   --ra --rm-archive - delete created archive, after it was sent

   --rf --rm-file - delete file after it was sent

   -h --help - display help message

=============
Sample output
=============
::

    transfer.sh_client|dev⚡ ⇒ transfer_files -f test.txt --rf

    Sending file: /home/path/to/directory/transfer.sh_client/test.txt (size of the file: 0.000113 MB)
    Link to download file(will be saved till 2017-09-16):
    https://transfer.sh/CtaJs/test.txt
    Link copied to clipboard
    Removing file... /home/path/to/directory/transfer.sh_client/test.txt
    Removed.



============
Download
============
::

  pip3 install transfersh_client

==================
Requirements
==================
 - pyperclip
 - requests

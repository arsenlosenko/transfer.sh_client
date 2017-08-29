# transfer.sh-uploader
Python client for uploading files to transfer.sh (https://transfer.sh/)

# Latest release:

https://pypi.python.org/pypi/transfersh-client/1.0.6

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
- After installation, you can run this package directly in command line:
~~~
transfer_files
~~~
- If you want to pass directory immediately, you can pass it as a parameter:
~~~
transfer_files /path/to/files
~~~

- Script will create archive of files in specified directory, upload it to transfer.sh, and provide this link to you, as well as copy it to clipboard.

File will be saved there for 14 days, it size should be less than 10 GB.
# Sample output

~~~
transfer.sh_client|dev⚡ ⇒ transfer_files ./
Creating zipfile from files in... ./
Added file:  requirements.txt
Added file:  client
Added file:  README.md
Added file:  README.rst
Added file:  setup.cfg
Added file:  .git
Added file:  setup.py
Added file:  LICENSE
Added file:  build
Added file:  .idea
Added file:  .gitignore

Sending zipfile:  files_archive_08-29_23:10.zip
Link to download zipfile:
 https://transfer.sh/rwnLy/files_archive_08-29_23:10.zip
Link copied to clipboard

Delete files in the directory?(y/n, Y/N, archive): archive
Deleting archive:  files_archive_08-29_23:10.zip
File removed
~~~



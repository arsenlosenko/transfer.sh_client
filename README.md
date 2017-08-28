# transfer.sh-uploader
Python client for uploading files to transfer.sh (https://transfer.sh/)

# Usage
- Start script
- Enter directory, which files you want to upload
- After download link received, confirm weather keep files in directory or delete them
- Share created download link where ever you want!

# Download
- Clone this repo
- Add required dependencies:

~~~~
pip3 -r requirements.txt
~~~~
   
- Create alias to this script (or start script manualy):

~~~
python3 transfer_file.py
~~~  

# Sample output

~~~
transfer.sh-uploader|master⚡ ⇒ transfer_files ./                                     
Creating zipfile from files in... ./
Added file:  README.md
Added file:  .idea
Added file:  requirements.txt
Added file:  transfer_file.py
Added file:  .git
Added file:  LICENSE

Sending zipfile:  files_archive_08-28_15:22.zip
Link to download zipfile:
 https://transfer.sh/eoqSx/files_archive_08-28_15:22.zip

 Delete files in the directory?(y/n, Y/N, archive): n
 OK, files will be there
~~~



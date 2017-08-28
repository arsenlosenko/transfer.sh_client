#!/usr/bin/python3
# EASY-INSTALL-ENTRY-SCRIPT: 'transfersh-uploader==0.0.1','console_scripts','transfer_files'
__requires__ = 'transfersh-uploader==0.0.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('transfersh-uploader==0.0.1', 'console_scripts', 'transfer_files')()
    )

from setuptools import setup, find_packages
from codecs import open
from os import path

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, 'README.md'), encoding="utf-8") as f:
    description = f.read()

setup(
    name="transfersh_uploader",
    version='0.0.1',
    description="transfer.sh command line client",
    url="https://github.com/arsenlosenko/transfer.sh-uploader",
    author="Arsen Losenko",
    author_email="arsenlosenko@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4'
    ],

    keywords='transfer.sh client uploader CLI',
    py_modules=['transfer_file'],
    entry_points={
            'console_scripts':[
                'transfer_files=transfer_file',
            ],
        },
    )



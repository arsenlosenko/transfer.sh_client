from setuptools import setup, find_packages
from os.path import join, dirname

setup(
        name="transfersh_client",
        version="1.1.0",
        author="Arsen Losenko",
        author_email="arsenlosenko@gmail.com",
        description="transfer.sh command-line client",
        url="https://github.com/arsenlosenko/transfer.sh_client.git",
        keywords="transfer.sh command-line client tool utility cli CLI",
        license="MIT",
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Utilities',
            'Environment :: Console',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5'
        ],
        packages=find_packages(),
        long_description=open(join(dirname(__file__), "README.rst")).read(),
        install_requires=[
            'requests==2.16',
            'pyperclip==1.5.27',
        ],
        entry_points={
                "console_scripts":
                ['transfer_files = client.app:main'],
            },
    )



from setuptools import setup, find_packages
from os.path import join, dirname


def list_requirements():
    deps = []
    requirements_file = "requirements.txt"
    with open(requirements_file) as f:
        for line in f.readlines():
            if "twine" in line:
                continue
                deps.append(line.strip())
    return deps


setup(
        name="transfersh_client",
        version="1.1.3",
        author="Arsen Losenko",
        author_email="arsenlosenko@protonmail.com",
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
        install_requires=list_requirements(),
        entry_points={
                "console_scripts":
                ['transfer_files = transfersh_client.app:main'],
            },
    )

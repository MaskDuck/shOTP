from re import M
from setuptools import setup
classifiers = [ "Development Status :: 2 - Pre-Alpha", "Intended Audience :: Developers", "Operating System :: Microsoft :: Windows :: Windows 10",]

setup(
    name='shotp',
    version='0.0.0a1',
    description='A command line interface that implements 2FA apps\' functionality.',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    classifiers=classifiers,
    packages=['shotp'],
    keywords=['otp', '2fa'],
    install_requires=['typer', 'shotp']
)
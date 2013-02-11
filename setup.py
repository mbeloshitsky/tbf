from distutils.core import setup

setup(
    name = "tbf",
    version = "0.1.14",
    author = "Michel Beloshitsky",
    author_email = "mbeloshitsky@gmail.com",
    packages = ['tbf'],
    url='',
    license='LICENSE.txt',
    description='Timed Boolean function utils',
    long_description = open('README.txt').read(),
    install_requires=['pyparsing >= 1.5']
)

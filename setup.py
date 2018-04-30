from setuptools import setup, find_packages

setup(
    name = 'TEDL',
    version = '0.0.6',
    description = 'TEDL Python Package',
    author = 'Duanfeng Gao',
    author_email = 'kevgao@live.com',
    url = 'http://tedesignlab.org/',
    license = "BSD",
    pacakges = find_packages(),
    install_requires = ['numpy','requests'],
)

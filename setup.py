from setuptools import setup, find_packages

install_requires = [
    'pandas>0.2',
    'gspread>=0.6.2',
    'oauth2client>=4.1.2',
]

setup(
        name = 'sheety',
        version = '0.2.1',
        author = 'James',
        packages = find_packages(),
        install_requires = install_requires,
        py_modules = ['sheety'],
)

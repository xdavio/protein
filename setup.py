from setuptools import setup, find_packages

setup(
    name='pdscript',
    version='0.1',
    py_modules=['pdscript', 'main','blockaverage','filter','pairdiff','process','ui','xmlreader'],
    install_requires=[
        'Click',
        'pandas',
        'numpy',
        'xlrd',
        'XlsxWriter'
    ],
    entry_points='''
        [console_scripts]
        pdscript=pdscript:diffmeas
    ''',
)

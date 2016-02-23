from setuptools import setup

setup(
    name='pdscript',
    version='0.1',
    py_modules=['pdscript'],
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

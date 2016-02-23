from setuptools import setup, find_packages

setup(
    name='pairdiff',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pandas',
        'numpy',
        'xlrd',
        'XlsxWriter'
    ],
    entry_points='''
        [console_scripts]
        pdscript=pairdiff.pdscript:diffmeas
    ''',
)

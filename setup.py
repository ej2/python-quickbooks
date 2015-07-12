from setuptools import setup, find_packages


VERSION = (0, 1, 0)
version = '.'.join(map(str, VERSION))

setup(
    name='python-quickbooks',
    version=version,
    author='Edward Emanuel Jr.',
    author_email='edward@sidecarsinc.com',
    description='A simple Python class for accessing the Quickbooks API.',
    url='https://github.com/sidecars/python-quickbooks',
    license='MIT',

    install_requires=[
        'setuptools',
        'rauth',
        'simplejson',
        'python-dateutil',
    ],

    packages=find_packages(),
)

from setuptools import setup, find_packages


VERSION = (0, 2, 6)
version = '.'.join(map(str, VERSION))

setup(
    name='python-quickbooks',
    version=version,
    author='Edward Emanuel Jr.',
    author_email='edward@sidecarsinc.com',
    description='A Python library for accessing the Quickbooks API.',
    url='https://github.com/sidecars/python-quickbooks',
    license='MIT',
    keywords=['quickbooks', 'qbo', 'accounting'],

    install_requires=[
        'setuptools',
        'rauth',
        'simplejson>=2.2.0',
        'six>=1.4.0',
        'python-dateutil',
    ],

    packages=find_packages(),
)

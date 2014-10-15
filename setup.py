from setuptools import setup, find_packages


VERSION = (0, 2)
version = '.'.join(map(str, VERSION))

setup(
    name='quickbooks',
    version=version,
    author='Simon Vansintjan',
    author_email='svansintjan@gmail.com',
    description='A really simple, brute-force, Python class for accessing the Quickbooks API.',
    url='https://github.com/simonv3/quickbooks-python',
    license='MIT',

    install_requires=[
        'setuptools',
        'rauth',
        'simplejson',
        'python-dateutil',
    ],

    packages=find_packages(),
)
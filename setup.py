import codecs
import os

from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


VERSION = (0, 8, 0)
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
    long_description=read('README.rst'),
    long_description_content_type='text/markdown',
    test_runner='nosetests',
    entry_points={
        'console_scripts': ['quickbooks-cli=quickbooks.tools.cli:cli_execute']
    },

    install_requires=[
        'setuptools',
        'intuit-oauth==1.2.2',
        'rauth>=0.7.1',
        'requests>=2.7.0',
        'simplejson>=2.2.0',
        'six>=1.4.0',
        'python-dateutil',
        'pycparser==2.18'
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(),
)

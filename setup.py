from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jinja_bs_modal',
    version='0.0.1',

    description='Jinja extension for rendering Bootstrap modals',
    long_description=long_description,
    url='https://github.com/uisky/jinja_bs_modal',
    author='Dmitry Romakhin',
    author_email='romakhin@gmail.com',
    license='LGPL',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Markup :: HTML',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    keywords='jinja bootstrap modal',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    py_modules=["jinja_bs_modal"],
    install_requires=['jinja2']
)
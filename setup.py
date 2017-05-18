import re
from setuptools import setup, find_packages

version = ''
with open('flask_py2neo.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='Flask-py2neo',
    version=version,
    url='url',
    license='MIT',
    author='Kyle Lawlor',
    author_email='klawlor419@gmail.com',
    description='A Flask extension for py2neo',
    zip_safe=False,
    packages=find_packages(),
    py_modules=['flask_py2neo'],
    install_requires=[
        'Flask>=0.7',
        'py2neo>3.0',
    ],
    tests_require=[
        'pytest>=3.0',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
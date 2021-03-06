from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import codecs
import os
import sys
import re

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = read('README.rst')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='bull',
    version=find_version('bull', '__init__.py'),
    url='http://github.com/jeffknupp/bull/',
    license='Apache Software License',
    author='Jeff Knupp',
    tests_require=['pytest'],
    install_requires=['Flask>=0.10.1',
                      'Flask-SQLAlchemy>=1.0',
                      'SQLAlchemy>=0.8.2',
                      'Flask-Admin>=1.0.7',
                      'Flask-Mail==0.9.0',
                      'Flask-SQLAlchemy==1.0',
                      'SQLAlchemy==0.9.1',
                      'stripe==1.11.0',
                      'Flask-WTF==0.9.4',
                      'Flask-Bcrypt==0.5.2',
                      'Flask-Login==0.2.9',
                      ],
    cmdclass={'test': PyTest},
    author_email='jeff@jeffknupp.com',
    description='Digital goods payment processing made simple',
    long_description=long_description,
    scripts=['scripts/bull'],
    packages=['bull'],
    package_dir={'bull': 'bull'},
    package_data={'bull': ['templates/*.html']},
    include_package_data=True,
    platforms='any',
    test_suite='tests.test_bull',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    extras_require={
        'testing': ['pytest'],
      }
)

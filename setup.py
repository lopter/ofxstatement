#!/usr/bin/python3
###############################################################################
#
# Copyright 2011 by CipherHealth, LLC
#
###############################################################################
"""Setup
"""
from setuptools import find_packages
from distutils.core import setup, Command
import unittest
import sys


class RunTests(Command):
    """New setup.py command to run all tests for the package.
    """
    description = "run all tests for the package"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        tests = unittest.TestLoader().discover('src')
        runner = unittest.TextTestRunner(verbosity=2)
        res = runner.run(tests)
        sys.exit(not res.wasSuccessful())


def get_version():
    initfname = 'src/ofxstatement/__init__.py'
    v = {}
    exec(compile(open(initfname).read(), initfname, 'exec'), globals(), v)
    return v['__version__']

with open("CHANGES.rst") as chlogf, open('README.rst') as rdmef:
    long_description = chlogf.read() + "\n\n" + rdmef.read()

setup(name='ofxstatement',
      version=get_version(),
      author="Andrey Lebedev",
      author_email="andrey@lebedev.lt",
      url="https://github.com/kedder/ofxstatement",
      description=("Tool to convert proprietary bank statement to "
                   "OFX format, suitable for importing to GnuCash"),
      long_description=long_description,
      license="GPLv3",
      keywords=["ofx", "banking", "statement"],
      cmdclass={'test': RunTests},
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU Affero General Public License v3'],
      packages=find_packages('src'),
      entry_points={
          'console_scripts':
          ['ofxstatement = ofxstatement.tool:run'],

          'ofxstatement':
          ['litas-esis = ofxstatement.plugins.litas_esis:LitasEsisPlugin',
           'swedbank = ofxstatement.plugins.swedbank:SwedbankPlugin',
           'danske = ofxstatement.plugins.danske:DanskePlugin',
           'maxibps = ofxstatement.plugins.maxibps:PSPlugin',
           'dkb_cc = ofxstatement.plugins.dkb_cc:DKBCCPlugin',
           'lbbamazon = ofxstatement.plugins.lbbamazon:LbbAmazonPlugin']
          },
      package_dir={'': 'src'},
      install_requires=['setuptools',
                        'appdirs'
                        ],
      extras_require={"test": ['mock']},
      include_package_data=True,
      zip_safe=True
      )

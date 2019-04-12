#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
import sys
if (sys.version_info < (3, 3)):
    sys.stderr.write("ERROR: pyaxe requires Python 3.3 or later\n")
    sys.exit(1)

import os

from configparser import ConfigParser
from distutils.command.clean import clean
from setuptools import find_packages, Command, setup
from setuptools.command.test import test as TestCommand
from setuptools.command.install import install
from subprocess import check_call, CalledProcessError

AXELIB_DIR = "cextern/aXe_c_code/"
CONF_H_NAME = os.path.join(AXELIB_DIR, "config.h")


# hack building the sphinx docs with C source
try:
    import sphinx
    from sphinx.setup_command import BuildDoc

    class BuildSphinx(BuildDoc):
        """Build Sphinx documentation after compiling C source files"""

        description = 'Build Sphinx documentation with C extensions'

        def initialize_options(self):
            BuildDoc.initialize_options(self)

        def finalize_options(self):
            BuildDoc.finalize_options(self)

        def run(self):
            build_cmd = self.reinitialize_command('build_ext')
            build_cmd.inplace = 1
            self.run_command('build_ext')
            sphinx.build_main(['setup.py', '-b', 'html',
                               './docs', './docs/_build/html'])

except ImportError:
    class BuildSphinx(Command):
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            sys.stderr.write('Sphinx is not installed!')
            exit(1)


class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [PACKAGENAME]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        try:
            import pytest
        except ImportError:
            print('Unable to run tests...')
            print('To continue, please install "pytest":')
            print('    pip install pytest')
            exit(1)

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class MyClean(Command):
    user_options = []

    def initialize_options(self):
        self.build_base = None
        self.build_lib = None
        self.build_temp = None
        self.build_scripts = None
        self.bdist_base = None
        self.all = None

    def finalize_options(self):
        self.set_undefined_options('build',
                                   ('build_base', 'build_base'),
                                   ('build_lib', 'build_lib'),
                                   ('build_scripts', 'build_scripts'),
                                   ('build_temp', 'build_temp'))
        self.set_undefined_options('bdist',
                                   ('bdist_base', 'bdist_base'))

    def run(self):
        print("** cleaning python and C binaries for aXe **")
        current_env = sys.prefix + "/bin/"
        axe_bins = ["aXe_SEX2GOL",
                    "aXe_GOL2AF",
                    "aXe_AF2PET",
                    "aXe_BE",
                    "aXe_PET2SPC",
                    "aXe_STAMPS",
                    "aXe_DRZPREP",
                    "aXe_PETCONT",
                    "aXe_PETFF",
                    "aXe_DRZ2PET",
                    "aXe_GPS",
                    "aXe_FILET",
                    "aXe_FRIGEN",
                    "aXe_FRINGECORR",
                    "aXe_TFIT",
                    "aXe_INTPIXCORR",
                    "aXe_PETIPC",
                    "aXe_NICBACK",
                    "aXe_TEST",
                    "aXe_DIRIMAGE",
                    "aXe_SCALEBCK"]

        try:
            check_call(["make", "clean"], cwd=AXELIB_DIR)
        except CalledProcessError as e:
            print(e)
            exit(1)

        for file in axe_bins:
            myfile = current_env + file
            if os.access(myfile, os.F_OK):
                os.remove(myfile)
        if os.access(CONF_H_NAME, os.F_OK):
            os.remove(CONF_H_NAME)

        clean.run(self)


class BuildExtWithConfigure(install):
    """Configure, build, and install the aXe C code."""
    user_options = install.user_options +\
        [('noremake', None, "Don't remake the aXe C executables [default True]")]

    def initialize_options(self):
        super().initialize_options()
        self.noremake = None
        self.remake = True

    def finalize_options(self):
        super().finalize_options()
        if self.noremake:
            if not os.access(AXELIB_DIR + "Makefile", os.F_OK):
                raise FileNotFoundError("Makefile doesn't exist, let axe build")
            else:
                self.remake = False

    def run(self):
        # only remake the C code if necessary
        # This is a simple check to see if a
        # Makefile already exists and skip
        if self.remake:
            CURRENT_ENV = sys.prefix
            try:
                check_call(["sh", "./configure",
                            "--with-cfitsio="+CURRENT_ENV,
                            "--with-wcstools="+CURRENT_ENV,
                            "--with-gsl="+CURRENT_ENV,
                            "--libdir="+CURRENT_ENV,
                            "--prefix="+CURRENT_ENV],
                           cwd=AXELIB_DIR)
                check_call(["make", "clean"], cwd=AXELIB_DIR)
                check_call(["make", "install"], cwd=AXELIB_DIR)
            except CalledProcessError as e:
                print(e)
                exit(1)

        install.run(self)

# Get some values from the setup.cfg
conf = ConfigParser()
conf.read(['setup.cfg'])
metadata = dict(conf.items('metadata'))
PACKAGENAME = metadata.get('package_name', 'pyaxe')
CLASSIFIER = metadata.get('classifier', 'Programming Language :: Python :: 3')
DESCRIPTION = metadata.get('description', 'aXe - spectral extraction for HST')
LONG_DESCRIPTION = metadata.get('long_description',
                                'aXe spectral extraction for HST minus the IRAF')
AUTHOR = metadata.get('author', 'STScI')
AUTHOR_EMAIL = metadata.get('author_email', 'https://hsthelp.stsci.edu')
LICENSE = metadata.get('license', '3-Clause BSD')
URL = metadata.get('url', 'http://axe-info.stsci.edu')


if os.path.exists('relic'):
    sys.path.insert(1, 'relic')
    import relic.release
else:
    try:
        import relic.release
    except ImportError:
        try:
            check_call(['git', 'clone',
                        'https://github.com/spacetelescope/relic.git'])
            sys.path.insert(1, 'relic')
            import relic.release
        except CalledProcessError as e:
            print(e)
            exit(1)

version = relic.release.get_info()
relic.release.write_template(version, PACKAGENAME)


# Note that requires and provides should not be included in the call to
# ``setup``, since these are now deprecated. See this link for more details:
# https://groups.google.com/forum/#!topic/astropy-dev/urYO8ckB2uM

setup(
    name=PACKAGENAME,
    version=version.pep386,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    classifiers=CLASSIFIER,
    install_requires=['numpy',
                      'astropy',
                      'wcstools',
                      'cfitsio',
                      'gsl',
                      'stwcs'],
    packages=find_packages(),
    tests_require=[
        'backports.tempfile',
        'pytest',
        'requests_mock',
        'pytest-catchlog'
    ],
    cmdclass={
        'test': PyTest,
        'build_sphinx': BuildSphinx,
        'build_ext': BuildExtWithConfigure,
        'install': BuildExtWithConfigure,
        'clean': MyClean,
    },
)

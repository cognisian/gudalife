#!/usr/bin/env python
import distutils.cmd
import distutils.log
import setuptools.command.build_py
from setuptools import setup

import os
import sys
import glob
import subprocess


class GResourcesCommand(distutils.cmd.Command):
    """A custom command to run glib-compile-resources on data/resources/*.xml"""

    description = 'run glib-compile-resources on GTK resource files'
    user_options = [
        ('gres-src-dir=', None, """Specify the source dir of gresource files specified in gresource xml files being compiled."""),
    ]

    def initialize_options(self):
        """Set default values for options."""
        self.gres_src_dir = 'data/resources'

    def finalize_options(self):
        """Post-process options."""
        print(self.gres_src_dir)
        if not os.path.isdir(self.gres_src_dir):
            raise Exception("Source resource directory does not exist: {0}".format(self.gres_src_dir))

    def run(self):
        """Run command."""
        self.announce('Starting build of gresources', level=distutils.log.INFO)

        # Get list of XML resource files
        resources = glob.glob('data/resources/*.xml')
        for res in resources:
            command = ['glib-compile-resources']
            command.append('%s' % res)
            command.append('--sourcedir')
            command.append(self.gres_src_dir)
            try:
                subprocess.call(command)
                self.announce(
                    'Built: %s' % str(command),
                    level=distutils.log.INFO)
            except:
                self.announce(
                    'Failed: %s' % str(command),
                    level=distutils.log.ERROR)


class GSchemasCommand(distutils.cmd.Command):
    """A custom command to run glib-compile-schemas on data/schema/*.xml"""

    description = 'run glib-compile-resources on GTK schema files'
    user_options = [
    ]

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        self.announce('Starting build of schemas', level=distutils.log.INFO)

        # Get list of XML schema files
        schemas = glob.glob('data/schemas/*.xml')
        for schema in schemas:
            command = ['glib-compile-schemas']
            command.append('%s' % schema)
            try:
                subprocess.call(command)
                self.announce(
                    'Built: %s' % str(command),
                    level=distutils.log.INFO)
            except:
                self.announce(
                    'Failed: %s' % str(command),
                    level=distutils.log.ERROR)


class BuildGTKCommand(setuptools.command.build_py.build_py):
    """Custom build command to include compiling gresources and gschemas."""

    def run(self):
        self.run_command('gresources')
        self.run_command('gschemas')
        setuptools.command.build_py.build_py.run(self)


APPNAME = 'gudalife'

# Autoconf like prefixs for FHS
prefix = '/usr'
if "--prefix" in sys.argv:
    index = sys.argv.index('--prefix')
    sys.argv.pop(index)
    prefix = sys.argv.pop(index)

bindir = '%s/bin/' % prefix
libexecdir = '%s/libexec' % prefix
sysconfdir = '%s/etc' % prefix
datarootdir = '%s/share' % prefix
datadir = datarootdir
infodir = '%s/info' % datadir
localedir = '%s/locale' % datadir
mandir = '%s/man' % datadir
docdir = '%s/doc/%s' % (datadir, APPNAME)

iconsrootdir = '%s/icons' % datadir
launcherdir = '%s/applications' % datadir
appdatadir = '%s/%s' % (datadir, APPNAME)
pkgdatadir = appdatadir


# Use requirements.txt file for dependencis to avoid duplicate def
required = []
with open('requirements.txt') as f:
    required = [l.strip('\n')
                for l in f if l.strip('\n') and not l.startswith('#')
    ]

# Do autoconf like macro replacement in main entry point script
gudalife = ''
with open('%s.in' % APPNAME) as f:
    # Replace @@ macros ala autoconf
    # f.read.replace()
    gudalife = f.read()
    gudalife = gudalife.replace('@datadir@', datadir)
    gudalife = gudalife.replace('@appdatadir@', appdatadir)
    gudalife = gudalife.replace('@localedir@', localedir)
    gudalife = gudalife.replace('@pkgdatadir@', pkgdatadir)
    with open('%s.py' % APPNAME, 'w') as fw:
        fw.write(gudalife)

setup(name=APPNAME,
      version='0.9.0',
      description="Conway's Game of Life on CUDA",
      author='Sean Chalmers',
      author_email='seandchalmers@yahoo.ca',
      url='http://www.cognisian.com',
      license='GPLv3',
      keywords='conway game life',
      long_description="Conway's Game of Life on CUDA",
      packages=[
          APPNAME
      ],
      install_requires=required,
      data_files=[
          (iconsrootdir + 'hicolor/256x256/apps', ['data/pixmaps/256x256/apps/*']),

          (launcherdir, ['data/gudalife.desktop']),
          (bindir, ['gudalife'])
      ],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Topic :: Desktop Environment :: Gnome',
        'Topic :: Games/Entertainment :: Board Games'
      ],
      cmdclass={
        'gresources': GResourcesCommand,
        'gschemas': GSchemasCommand,
        'build_py': BuildGTKCommand,
      },
)

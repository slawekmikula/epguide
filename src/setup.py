__author__="zorba"
__date__ ="$2009-09-26 20:50:59$"

from setuptools import setup,find_packages

setup (
  name = 'epguide',
  version = '1.0',
  packages = find_packages(),
  package_data = {'': 'AUTHORS', '': 'COPYING', '': 'ChangeLog', '': 'README' },

  # Declare your packages' dependencies here, for eg: foo>=3
  install_requires=[''],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'Slawek Mikula',
  author_email = 'slawek.mikula@gmail.com',

  summary = 'Python Electronic TV Guide Downloader and XMLTV exporter',
  url = 'code.google.com/p/epguide',
  license = 'GNU GPLv2',
  long_description= '',
  
)
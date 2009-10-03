__author__="zorba"
__date__ ="$2009-09-26 20:50:59$"

from setuptools import setup,find_packages

setup (
    name = 'epguide',
    version = '1.0',
    packages = find_packages(exclude=['bin','test']),
    package_data = {'': ['AUTHORS', 'LICENSE',
    'CHANGES', 'README']},

    # Declare your packages' dependencies here, for eg: foo>=3
    install_requires=[''],

    # Fill in these to make your Egg ready for upload to
    # PyPI
    author = 'Slawek Mikula',
    author_email = 'slawek.mikula@gmail.com',

    url = 'http://code.google.com/p/epguide',
    download_url = "http://code.google.com/p/epguide",

    description = 'Python Electronic TV Guide Downloader and XMLTV exporter',
    long_description= '',

    keywords = ["xmltv", "channels", "tv guide"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Text Processing :: Markup :: XML",
        ],

    entry_points="""
  [console_scripts]
  epguide = epguide.epg_runner:RunEpguide
  """,

)
__author__="smikula"
__date__ ="$2012-05-31 18:30:00$"

from setuptools import setup, find_packages

setup (
    name = 'epguide',
    version = '1.9.3',
    packages = find_packages(exclude=['bin','test']),
    package_data = {'': ['AUTHORS', 'LICENSE',
    'CHANGES', 'README', 'epguide_run']},

    # Declare your packages' dependencies here, for eg: foo>=3
    install_requires=['lxml>=2.3.5', 'ConfigObj', 'httplib2>=0.8'],

    # Fill in these to make your Egg ready for upload to PyPI
    author = 'Slawek Mikula',
    author_email = 'slawek.mikula@gmail.com',

    url = 'http://code.google.com/p/epguide',
    download_url = "http://code.google.com/p/epguide",

    description = 'Python Electronic TV Guide (EPG) Downloader and XMLTV exporter for Polish TV',
    long_description= '',

    keywords = ["xmltv", "channels", "tv guide", "epg", "tv", "grabber"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Text Processing :: Markup :: XML",
        ],

    entry_points= {"console_scripts": 
                   ["epguide = epguide.epg_runner:RunEpguide", 
                    "tv_grab_pl_epguide = epguide.tv_grab_pl_epguide:RunTvGrabPlEpguide"]}
)

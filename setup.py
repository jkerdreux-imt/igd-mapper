from setuptools import setup,find_packages

with open('README.md') as f:
    long_description = f.read()

VERSION = "0.1"

setup(
    name='igd-mapper',
    version=VERSION,
    license='GPL License',
    author='Jerome Kerdreux',
    author_email='Jerome.Kerdreux@imt-atlantique.fr',
    #url='',
    description=('Python script to automate UPnP port mapping'),
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['upnp', 'igd','nat'],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,

    entry_points = {
      'console_scripts': [
          'idg-mapper = src.app:main',
      ]
    },
    install_requires=[
        'miniupnpc',
        'configobj',
    ]
)


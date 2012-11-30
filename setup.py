from setuptools import setup, find_packages

version = '0.1'

setup(name='osmread',
      version=version,
      description="Simple library for reading OpenStreetMap XML and PBF data files",
      long_description="""""",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Operating System :: OS Independent",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries",
          "Topic :: Scientific/Engineering :: GIS",
      ],
      author='Aleksandr Dezhin',
      author_email='me@dezhin.net',
      url='http://github.com/dezhin/osmread',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'argparse',
          'protobuf',
          'lxml',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      osmread = osmread.script:main
      """
      )

from distutils.core import setup
setup(
  name = 'dwpoints',
  packages = ['dwpoints'],
  version = '0.0.0.1',
  description = 'DW Points: Generate DW values for specific points',
  author = 'Brookie Guzder-Williams',
  author_email = 'bguzder-williams@wri.org',
  url = 'https://github.com/wri/dwpoints',
  download_url = 'https://github.com/wri/dwpoints/tarball/0.1',
  keywords = ['dynamicworld','landcover'],
  include_package_data=True,
  data_files=[
    (
      'config',[]
    )
  ],
  classifiers = [],
  entry_points={
      'console_scripts': [
          'dwpoints=dwpoints.cli:cli',
          'dwpointsemote=dwpoints.cli:cli'
      ]
  }
)
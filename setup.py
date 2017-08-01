from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='lcmap-merlin',
      version='0.5.2',
      description='Python client library for LCMAP-Aardvark',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: Public Domain',
        'Programming Language :: Python :: 3.6',
      ],
      keywords='usgs lcmap eros',
      url='http://github.com/usgs-eros/lcmap-merlin',
      author='USGS EROS LCMAP',
      author_email='',
      license='Unlicense',
      packages=['merlin'],
      install_requires=[
          'numpy',
          'requests',
          'python-dateutil',
      ],
      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[test]
      extras_require={
          'test': ['pytest',
                   'hypothesis',
                   'mock',
                  ],
          'dev': ['jupyter',],
      },
      # entry_points={
          #'console_scripts': [''],
      # },
      include_package_data=True,
      zip_safe=False)

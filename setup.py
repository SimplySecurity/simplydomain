from setuptools import setup, find_packages


VERSIONFILE = open("VERSION").read()

setup(name='simplydomain',
      version=VERSIONFILE,
      description='simplydomain is a very basic framework to automate domain brute forcing.',
      url='http://github.com/SimplySecurity/simplydomain-pkg',
      author='Alexander Rymdeko-Harvey',
      author_email='a.rymdekoharvey@obscuritylabs.com',
      license='BSD 3.0',
      packages=[
          'simplydomain',
          'simplydomain.src',
          'simplydomain.src.dynamic_modules',
          'simplydomain.src.static_modules',
          'simplydomain.tests'
      ],
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 4 - Beta',
          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'
      ],
      install_requires=[
          'aiodns',
          'beautifulsoup4',
          'crtsh',
          'dnsdumpster',
          'fake_useragent',
          'json2xml',
          'requests',
          'setuptools',
          'termcolor',
          'tqdm',
          'uvloop',
          'validators',
          'click'
      ],
      scripts=[
          'simplydomain/bin/simply_domain.py'
      ],
      include_package_data=True,
      zip_safe=False)

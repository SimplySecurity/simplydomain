from setuptools import setup, find_packages

setup(name='SimplyDomain',
      version='1.1.7',
      description='SimplyDomain is a very basic framework to automate domain brute forcing.',
      url='http://github.com/SimplySecurity/SimplyDomain',
      author='Alexander Rymdeko-Harvey',
      author_email='a.rymdekoharvey@obscuritylabs.com',
      license='BSD 3.0',
      packages=[
          'SimplyDomain',
          'SimplyDomain.src',
          'SimplyDomain.modules',
          'SimplyDomain.tests',
      ],
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
     ],
      install_requires=[
        'beautifulsoup4 == 4.6.0',
        'crtsh == 0.1.0',
        'dnsdumpster == 0.3',
        'fake_useragent == 0.1.8',
        'json2xml == 2.2.0',
        'requests == 2.18.4',
        'setuptools == 32.2',
        'termcolor == 1.1.0',
        'validators == 0.12.0'
              ],
      scripts=[
          'SimplyDomain/SimplyDomain.py'
      ],
      zip_safe=False)

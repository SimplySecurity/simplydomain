from setuptools import setup

setup(name='SimplyDomain',
      version='1.0',
      description='SimplyDomain is a very basic framework to automate domain brute forcing.',
      url='http://github.com/SimplySecurity/SimplyDomain',
      author='Alexander Rymdeko-Harvey',
      author_email='a.rymdekoharvey@obscuritylabs.com',
      license='BSD 3.0',
      packages=['SimplyDomain'],
      install_requires=[
          '',
      ],
      scripts = [
        'SimplyDomain/SimplyDomain.py'
      ],
      zip_safe=False)
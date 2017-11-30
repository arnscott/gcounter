from setuptools import setup

version = '0.0.01'


namespace_packages = ['lib', 'gcounter']

packages = ['lib.csv',
            'lib.queries',
            'lib.sqlite',
            'gcounter.utils',
            'gcounter/analysis']


scripts = ['bin/process-vcf',
           'bin/process-sam',
           'bin/load-db',
           'bin/identify-variants',
           'bin/count-possible-genomes']


install_requires = ['setuptools',
                    'requests',
                    'BeautifulSoup4 >= 4.0.0']


setup(name='gcounter',
      version=version,
      namespace_packages=namespace_packages,
      packages=packages,
      scripts=scripts,
      license='open',
      author='Aaron Scott',
      author_email='aa5278sc-s@student.lu.se',
      install_requires=install_requires)

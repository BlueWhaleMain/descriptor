from distutils.core import setup

from setuptools import find_packages

with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(name='descriptor',
      version='1.0.0',
      description='A descriptor package',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      author='BlueWhaleMain',
      author_email='bluewhalemain@outlook.com',
      python_requires='>=3.6.0',
      url='',
      packages=find_packages(),
      install_requires=[],
      # extras_require=[],
      include_package_data=True,
      license='MIT License',
      platforms=['all'],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development :: Libraries'
      ],
      )

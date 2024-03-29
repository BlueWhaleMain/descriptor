from distutils.core import setup

from setuptools import find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(name='field-descriptor',
      version='1.0.1',
      description='A descriptor package',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='BlueWhaleMain',
      author_email='bluewhalemain@outlook.com',
      python_requires='>=3.6.0',
      url='https://github.com/BlueWhaleMain/descriptor',
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
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries'
      ],
      )

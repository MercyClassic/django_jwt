from setuptools import setup, find_packages

VERSION = '1.1.0'


setup(
    name='django_jwt',
    version=VERSION,
    packages=find_packages(),
    package_dir={'django_jwt': 'django_jwt'},
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MercyClassic/django_jwt',
    author='MercyClassic',
    requires=['django', 'PyJWT'],
)

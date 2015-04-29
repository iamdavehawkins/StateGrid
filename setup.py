from distutils.core import setup

setup(
    name='StateGrid',
    version='0.1',
    author='David Hawkins',
    author_email='iamdavehawkins@gmail.com',
    packages=['stategrid',],
    license='LICENSE.txt',
    install_requires=[
        'matplotlib>=1.4.2',
        'pandas>=0.15.2',
        'numpy>=1.9.2rc1']
)
from setuptools import setup

setup(
    name='money-manager',
    version='0.0.1',
    packages=[''],
    url='https://github.com/TashaGospel/money-manager',
    license='MIT',
    author='alanspringfield',
    author_email='',
    description='A little script for me to keep track of my spending.',
    install_requires=[
        'Click'
    ],
    entry_points="""
        [console_scripts]
        money-manager=main:cli
    """
)

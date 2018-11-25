from setuptools import setup

setup(
    name='jas',
    entry_points={
        'console_scripts': [
            'wiki=wiki:cli'
        ],
    },
)
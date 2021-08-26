from setuptools import setup

def _get_requires():
    with open('requirements.txt') as f:
        return f.readlines()

setup(
    name='logen',
    version='0.0.1',
    url='https://github.com/pbandj082/logen',
    packages=['logen'],
    requires=_get_requires(),
    extras_requires={
        'dev': ['pytest']
    },
)
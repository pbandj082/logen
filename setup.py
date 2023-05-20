from setuptools import setup

def _get_requires():
    with open('requirements.txt') as f:
        return [p.rstrip() for p in f.readlines()]


setup(
    name='logen',
    version='0.0.13',
    url='https://github.com/pbandj082/logen',
    packages=['logen', 'logen.adapters', 'logen.adapters.logging'],
    requires=_get_requires(),
)

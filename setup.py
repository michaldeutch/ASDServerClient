from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='ASDServerClient',
    version='0.1.0',
    packages=find_packages(),
    author='Michal Deutch',
    description='A server-client interface ',
    install_requires=required,
    test_require=['pytest']
)

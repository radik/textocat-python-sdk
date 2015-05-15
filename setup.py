from setuptools import setup, find_packages

setup(
    name='textocat',
    version='0.1.2',
    description='Unofficial Textocat Python SDK',
    url='http://github.com/radik/textocat-python-sdk',
    author='Radik Fattakhov',
    author_email='radikft@gmail.com',
    license='Apache License, Version 2.0',
    packages=find_packages(exclude=['examples', 'docs', 'tests*']),
    install_requires=['requests>=2.7.0'],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    extras_require={
        'test': ['httpretty'],
    },
)
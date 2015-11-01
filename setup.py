from setuptools import setup, find_packages

setup(
    name='edge',
    version='0.0.1',
    packages=find_packages(include=('edge', 'edge.*')),
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=('nose', 'nose-parameterized',),
    requires=['networkx'],
    license='MIT',
    test_suite='tests',
    classifiers=(
        'Programming Language :: Python',
        'License :: MIT',
        'Natural language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Graph Theory',
    )
)

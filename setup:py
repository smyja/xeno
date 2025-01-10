from setuptools import setup, find_packages

setup(
    name='ocli',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'ocli=ocli.cli:main',
        ],
    },
    install_requires=[
        'click>=8.0.0',
        'rich>=10.0.0',
    ],
    python_requires='>=3.7',
)
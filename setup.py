"""
Setup script for the Aphra package.

This script uses setuptools to package and distribute the Aphra package, which
provides translation functionality using LLMs (Large Language Models).
"""

from setuptools import setup, find_packages

setup(
    name='aphra',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'openai>=1.40.2',
        'toml>=0.10.2',
        'requests>=2.32.3'
    ],
    entry_points={
        'console_scripts': [
            'aphra-translate=aphra.translate:main',
        ],
    },
    package_data={
        'aphra': ['prompts/*.txt'],
    },
    include_package_data=True,
    description='A translation package using LLMs',
    author='DavidLMS',
    author_email='dobles-establecer-0m@icloud.com',
    url='https://github.com/DavidLMS/aphra',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

from setuptools import setup, find_packages

setup(
    name='aphra',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'openai',
        'toml',
        'requests',
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
    author='David Romero',
    author_email='hola@davidlms.com',
    url='https://github.com/DavidLMS/aphra',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
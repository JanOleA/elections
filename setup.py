from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as infile:
    long_description = infile.read()

setup(
    name='pylections',
    version='0.1.0',
    author='Jan Ole Fiksdal Åkerholm',
    author_email='janole@akerholm.no',
    packages=['elections'],
    license='LICENSE.txt',
    description='Simple election analysis tools',
    long_description=long_description,
    install_requires=[
        'numpy',
        'pandas',
    ],
    python_requires='>=3.7',
)
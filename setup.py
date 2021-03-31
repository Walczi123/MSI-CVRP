from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
)

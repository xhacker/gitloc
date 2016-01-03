# This is not purely the result of trial and error.

from setuptools import setup, find_packages

setup(
    name="gitloc",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "gitloc = gitloc.__main__:main",
        ],
    },

    author="Dongyuan Liu",
    author_email="liu.dongyuan@gmail.com",
    description="Count line of code for a certain time period and a certain author in a git repository.",
    license="MIT",
    keywords="git loc line code author contributor contribution",
    url="https://github.com/xhacker/gitloc",
)

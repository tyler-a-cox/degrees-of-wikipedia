#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

requirements = ["cmasher", "twython", "numpy", "matplotlib", "scipy"]
test_requirements = requirements

setup(
    author="Tyler Cox",
    author_email="tyler.a.cox@berkeley.edu",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Twitter bot that posts springy double pendulum simulations to twitter",
    entry_points={"console_scripts": ["xcorr=xcorr.cli:main",],},
    install_requires=requirements,
    license="BSD license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="pyelastic",
    name="pyelastic",
    packages=find_packages(include=["pyelastic", "pyelastic.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/tyler-a-cox/elastic-pendulum",
    version="0.1.0",
    zip_safe=False,
)
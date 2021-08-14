#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

requirements = ["asyncio", "aiohttp", "numpy"]
test_requirements = requirements

setup(
    author="Tyler Cox",
    author_email="tyler.a.cox@berkeley.edu",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Twitter bot that posts springy double pendulum simulations to twitter",
    entry_points={"console_scripts": ["wikiracer=wikiracer.cli:main",],},
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords="wikiracer",
    name="wikiracer",
    packages=find_packages(include=["wikiracer", "wikiracer.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/tyler-a-cox/degrees-of-wikipedia",
    version="0.1.0",
    zip_safe=False,
)

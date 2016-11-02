from setuptools import setup, find_packages

with open('README') as f:
    long_description = ''.join(f.readlines())

setup(
    author="Martin Chovanec",
    author_email="chovamar@fit.cvut.cz",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet"
    ],
    description="Twitter reader",
    long_description=long_description,
    license="MIT License",
    url="https://github.com/chovanecm/mi-pyt1",
    name="simpletwitter",
    keywords="twitter,reader",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "simpletwitter = simpletwitter.twitter_main:main"
        ]
    },
    install_requires=["Flask", "click>=6"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "betamax"],
    version="0.4"
)

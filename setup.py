from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = "digitaltwin_on_fhir"
LONG_DESCRIPTION = "A package for fhir adapter in digital twins platform."

setup(
    # the name must match the package name - verysimpletest
    name="digitaltwin_on_fhir",
    version=VERSION,
    author="LinkunGao",
    author_email="gaolinkun123@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    # Add any packages if you use it in your packages
    install_requires=[
        "fhirpy>=1.4.2",
        "pydicom>=2.4.3",
        "pathlib>=1.0.1"
    ],
    keywords=['digitaltwin', 'fhir', 'python'],
    classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "License :: OSI Approved :: Apache Software License"
    ]
)
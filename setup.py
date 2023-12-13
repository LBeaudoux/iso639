import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iso639-lang",
    version="2.2.2",
    author="L.Beaudoux",
    description="A lightweight library for the ISO 639 standard.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LBeaudoux/iso639",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    python_requires=">=3.7",
    package_data={"iso639": ["data/*.json", "data/*.pkl"]},
    install_requires=[
        "importlib-resources;python_version<'3.9'",
    ],
)

import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iso639-lang",
    version="0.0.6",
    author="L.Beaudoux",
    description="A simple library for ISO 639 language codes.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/l-bdx/iso639",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.6",
    package_data={"": ["*.tab"]},
)

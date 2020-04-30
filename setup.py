import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iso639-l-bdx",
    version="0.0.1",
    author="Laurent Beaudoux",
    author_email="lbeaudoux@gmail.com",
    description="A Python 3.6 library for ISO 639 language codes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/l-bdx/iso639",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
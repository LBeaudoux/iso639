import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iso639-lang",
    version="2.3.0",
    author="Laurent Beaudoux",
    author_email="lbeaudoux@gmail.com",
    description="A fast, simple ISO 639 library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LBeaudoux/iso639",
    keywords=[
        "ISO 639",
        "ISO 639-1",
        "ISO 639-2",
        "ISO 639-3",
        "ISO 639-5",
        "language code",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Localization"
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    packages=["iso639"],
    package_data={"iso639": ["data/*.json"]},
    install_requires=[
        "importlib-resources;python_version<'3.9'",
    ],
)

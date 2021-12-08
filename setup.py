import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiogram-pagination",
    version="0.1",
    author="altroncode",
    author_email="cosmosx1328@gmail.com",
    description="Module for deep pagination in an aiogram bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/altroncode/aiogram-pagination",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries'

    ],
    # install_requires=[
    #     'aiogram>=2.16',
    #     'bestconfig>=1.3.5',
    # ]
)

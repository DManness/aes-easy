import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aes-easy",
    version="1.0.0",
    author="DManness",
    author_email="",
    description="A cryptography wrapper making encrypting with AES easy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmanness/aes-easy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)
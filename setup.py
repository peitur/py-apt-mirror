import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-apt-mirror",
    version="0.0.1",
    author="Peter Bartha",
    author_email="peitur@gmail.com",
    description="Python based APT repository mirror tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peitur/py-apt-mirror",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
)

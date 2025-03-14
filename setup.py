from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="TerraForge",
    version="0.1.0",
    author="Saba Momtselidze",
    author_email="sabamomtselidze@gmail.com",
    description="A library for generating and manipulating Terraform configurations in HCL format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Elmo33/terraforge",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license="Apache License 2.0",
    python_requires='>=3.6',
)

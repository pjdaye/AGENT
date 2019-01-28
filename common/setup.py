import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aist_common",
    version="0.0.1",
    author="Ultimate Software",
    author_email="quality@ultimatesoftware.com",
    description="Common Python libraries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UltimateSoftware/AGENT",
    packages=setuptools.find_packages(),
    data_files=[('grammar', ['aist_common/grammar/seq.g'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)
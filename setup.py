import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Chai.py", # Replace with your own username
    version="1.0",
    author="蓝落萧",
    author_email="2320693692@qq.com",
    description="汉字自动拆分系统",
    install_requires=['PyYAML'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL3 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


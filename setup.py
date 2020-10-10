import setuptools

with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pychai',
    version='1.0.1',
    author='hanzi-chai',
    author_email='2320693692@qq.com',
    description='A System for Automatic Chinese Character Decomposition',
    install_requires=['PyYAML', 'numpy'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hanzi-chai/chai',
    packages=setuptools.find_packages(),
    package_data={'': ['*.py', '*.yaml']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)

from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='buff2steam',
    version='0.3.1',
    python_requires='>=3.7',
    url='https://github.com/hldh214/buff2steam',
    license='Unlicense',
    description='Yet another steam trade bot w/ buff.163.com',
    long_description=long_description,
    packages=['buff2steam'],
    install_requires=[
        'httpx',
        'loguru',
        'tenacity'
    ],
    author='Jim',
    author_email='hldh214@gmail.com',
)

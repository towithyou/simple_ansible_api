from setuptools import setup
from simple_ansible_api import __version__

ABSIBLE_REQUIRE = '2.10.0'


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='simple-ansible-api',
    version=__version__,
    author='Haiquan',
    author_email='haiquanduan@gmail.com',
    description='This is a sample package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['simple_ansible_api',],
    keywords='ansible',
    url='https://github.com/towithyou/simple_ansible_api',
    install_requires=[
        'ansible>=' + ABSIBLE_REQUIRE
    ],
    requires=["ansible"],
    zip_safe=False,
    include_package_data=True,
)
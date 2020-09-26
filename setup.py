from setuptools import setup
from setuptools.command.install import install
import os
import sys


ABSIBLE_REQUIRE = '2.10.0'


class CustomInstall(install):
    def run(self):
        os.system("%s -m pip install ansible>=%s" % (sys.executable, ABSIBLE_REQUIRE))


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='simple-ansible-api',
    version='v1.1',
    author='Haiquan',
    author_email='haiquanduan@gmail.com',
    description='This is a sample package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    cmdclass={'install': CustomInstall},
    license='MIT',
    packages=['simple_ansible_api',],
    keywords='ansible',
    url='https://github.com/towithyou/simple_ansible_api',
    install_requires=[
        'ansible>=' + ABSIBLE_REQUIRE
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any'
)
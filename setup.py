import re
import os.path
from setuptools import setup, find_packages

_here = os.path.abspath(os.path.dirname(__file__))
requirements_path = os.path.join(_here, 'requirements', 'requirements.txt')
test_requirements_path = os.path.join(_here, 'requirements', 'test_requirements.txt')


def get_requirments(path):
    with open(path, 'rt') as f:
        data = f.read()
    return re.findall(r"[A-Za-z][A-Za-z0-9\-\.]+==[0-9\.\-A-Za-z]*", data)


requirements = get_requirments(requirements_path)
tests_require = get_requirments(test_requirements_path)

setup(
    name="movie_list-api",
    version="1.0.0",
    install_requires=requirements,
    zip_safe=False,
    packages=find_packages(),
    extras_require={"dev": tests_require, "test": tests_require},
)

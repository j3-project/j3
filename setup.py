import os
import j3
from os import path

from setuptools import setup


def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        if "__pycache__" in path:
            continue
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


extra_files = package_files("j3/templates")

this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, "README.md")) as f:
    long_description = f.read()

version = j3.__version__

setup(
    name="J3 Framework",
    description="J3 Framework - full-stack framework for microservice architecture applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    license="MIT",
    author="Joseph Kim",
    author_email="cloudeyes@gmail.com",
    packages=["j3", "j3.test", "j3.core"],
    package_data={
        "": extra_files,
        "j3": ["py.typed"],
        "j3.core": ["py.typed"],
        "j3.test": ["py.typed"],
    },
    url="https://gihub.com/j3-project/j3",
    download_url=f"https://github.com/j3-project/j3/archive/v{version}.tar.gz",
    keywords=["j3", "microservice" "framework", "sqlalchemy", "fastapi"],
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "uvicorn",
        "jinja2",
        "colorama",
        "tenacity",
        "aioredis",
        "httpx",
        "requests",  # starlette's dependency for TestClient
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        "console_scripts": [
            "j3 = j3.command:console_main",
        ]
    },
)

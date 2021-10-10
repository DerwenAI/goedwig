# type: ignore

"""
Python packaging.
"""

import importlib.util
import pathlib
import typing

import setuptools


KEYWORDS = [
    "cypher",
    "query optimization",
    "graph query",
    "knowledge graph",
    ]


def parse_requirements_file (filename: str) -> typing.List:
    """read and parse a Python `requirements.txt` file, returning as a list of str"""
    with pathlib.Path(filename).open() as f:  # pylint: disable=C0103
        return [ l.strip().replace(" ", "") for l in f.readlines() ]


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("goedwig.version", "goedwig/version.py")
    goedwig_version = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(goedwig_version)
    MIN_PY_VERSION = ".".join([ str(x) for x in goedwig_version.MIN_PY_VERSION ])

    base_packages = parse_requirements_file("requirements.txt")
    docs_packages = parse_requirements_file("requirements-dev.txt")

    setuptools.setup(
        name = "goedwig",
        version = goedwig_version.__version__,
        python_requires = ">=" + MIN_PY_VERSION,

        packages = setuptools.find_packages(exclude=[ "docs", "examples" ]),
        install_requires = base_packages,
        extras_require = {
            "base": base_packages,
            "docs": docs_packages,
            },

        author = "Paco Nathan",
        author_email = "paco@derwen.ai",
        license = "MIT",

        description = "A generic query engine for graph data, based on abstract syntax trees as input.",  # pylint: disable=C0301
        long_description = pathlib.Path("README.md").read_text(),
        long_description_content_type = "text/markdown",

        keywords = ", ".join(KEYWORDS),
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Scientific/Engineering :: Human Machine Interfaces",
            "Topic :: Scientific/Engineering :: Information Analysis",
            ],

        url = "https://github.com/DerwenAI/goedwig",
        project_urls = {
            "Source Code": "https://github.com/DerwenAI/goedwig",
            "Issue Tracker": "https://github.com/DerwenAI/goedwig/issues",
            },

        zip_safe = False,
        )

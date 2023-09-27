Installation
============

You can install this package via poetry:

   pip install poetry
   poetry install

It is also available on PyPI ([link](https://pypi.org/project/puggle/)), so rather than cloning this repo, you can install it via pip:

   pip install puggle

To be able to use the `load_into_neo4j` function from the `Dataset` class, you will need to have Neo4j installed and running on your machine. The easiest way to do this is via Docker, though in the interest of keeping this package light we do not include a dockerfile here.

To use the `load_into_neo4j` function you also need to set an environment variable for your Neo4j password. You can do this by creating an empty `.env` file in the root directory of this repository and including:

   NEO4J_PASSWORD=<your neo4j password>


Puggle
======

.. success::

    Full README available on `ReadtheDocs <https://puggle.readthedocs.io/en/latest/>`_.

This library is designed to provide utilities for working with the outputs of entity typing models such as `SPERT <https://github.com/lavis-nlp/spert/>`_, `E2EET <https://github.com/Michael-Stewart-Webdev/e2e-entity-typing>`_, or annotation tools such as `Quickgraph <https://quickgraph.tech/>`_. Puggle has three main purposes:

 * Provide easy parsing of the output (i.e. annotations) of entity typing models
 * Enable the connection between structured data (csv) and those annotations
 * Provide functionality to easily load the structured data + annotations into a Neo4j graph

We do not include any code for actually running machine learning models here. Puggle is purely designed for loading the results of such models into Python-based classes and then easily importing the data into Neo4j.

Full documentation available on `ReadtheDocs <https://puggle.readthedocs.io/en/latest/>`_.
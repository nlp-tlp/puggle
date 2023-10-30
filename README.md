# Puggle

This library is designed to provide utilities for working with the outputs of entity typing models such as [SPERT](https://github.com/lavis-nlp/spert/), [E2EET](https://github.com/Michael-Stewart-Webdev/e2e-entity-typing), or annotation tools such as [Quickgraph](https://quickgraph.tech/). Puggle has three main purposes:

-   Provide easy parsing of the output (i.e. annotations) of entity typing models
-   Enable the connection between structured data (csv) and those annotations
-   Provide functionality to easily load the structured data + annotations into a Neo4j graph

We do not include any code for actually running machine learning models here. Puggle is purely designed for loading the results of such models into Python-based classes and then easily importing the data into Neo4j.

Full documentation available on [ReadtheDocs](https://puggle.readthedocs.io/en/latest/). Please checkout this page for the full readme.

## Why is it called Puggle?

This is a super lightweight version of [Echidna](https://github.com/nlp-tlp/mwo2kg-and-echidna), our software application for constructing knowledge graphs from unstructured text. A puggle is a baby Echidna, so it seemed appropriate!

It also works as an acronym!

Puggle = Python Utilities for Generating Graphs from Linked Entities

## TODO

-   Automatic parsing of dates, floats, etc, when building the Neo4j graph
-   A function in the `Dataset` class (`create_neo4j_csvs()`) to create CSVs to import into Neo4j, so that they can be created and then imported later/elsewhere
-   Unit tests

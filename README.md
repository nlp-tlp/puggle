# Puggle

[![Coverage Status](https://coveralls.io/repos/github/nlp-tlp/puggle/badge.svg?branch=data_utils)](https://coveralls.io/github/nlp-tlp/puggle?branch=data_utils)

This library is designed to provide utilities for working with the outputs of entity typing models such as [SPERT](https://github.com/lavis-nlp/spert/), [E2EET](https://github.com/Michael-Stewart-Webdev/e2e-entity-typing), or annotation tools such as [Quickgraph](https://quickgraph.tech/). Puggle has three main purposes:

-   Provide easy parsing of the output (i.e. annotations) of entity typing models
-   Enable the connection between structured data (csv) and those annotations
-   Provide functionality to easily load the structured data + annotations into a Neo4j graph

We do not include any code for actually running machine learning models here. Puggle is purely designed for loading the results of such models into Python-based classes, (optionally) manipulating that data, and then easily importing the data into Neo4j.

<p align="center">:blue_book: :green_book: :orange_book: <strong>Full README and code documentation available on <a href="https://puggle.readthedocs.io/en/latest/">ReadtheDocs</a>.</strong> :orange_book: :green_book: :blue_book:</p>

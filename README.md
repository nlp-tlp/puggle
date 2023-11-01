# Puggle

[![Pytest Status](https://github.com/nlp-tlp/puggle/actions/workflows/run-tests.yml/badge.svg)](https://github.com/nlp-tlp/puggle/actions/workflows/run-tests.yml) [![Coverage Status](https://coveralls.io/repos/github/nlp-tlp/puggle/badge.svg?branch=main)](https://coveralls.io/github/nlp-tlp/puggle?branch=main) [![Pylint Status](https://github.com/nlp-tlp/badges/blob/main/puggle-pylint-badge.svg)](https://github.com/nlp-tlp/puggle/actions/workflows/run-pylint.yml)

This library is designed to provide utilities for working with the outputs of entity typing models such as [SPERT](https://github.com/lavis-nlp/spert/), [E2EET](https://github.com/Michael-Stewart-Webdev/e2e-entity-typing), or annotation tools such as [Quickgraph](https://quickgraph.tech/). Puggle has three main purposes:

-   Provide easy parsing of the output (i.e. annotations) of entity typing models
-   Enable the connection between structured data (csv) and those annotations
-   Provide functionality to easily load the structured data + annotations into a Neo4j graph

We do not include any code for actually running machine learning models here. Puggle is purely designed for loading the results of such models into Python-based classes, (optionally) manipulating that data, and then easily importing the data into Neo4j.

<p align="center">📘📗📙 <strong>Full README and code documentation available on <a href="https://puggle.readthedocs.io/en/latest/">ReadtheDocs</a>.</strong> 📙📗📘</p>

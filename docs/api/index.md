(api)=

(reference)=

# API Reference

cihai's public API for CJK character lookups and dataset management.

:::{warning}
cihai is pre-1.0. APIs may change between minor versions. Pin to a range:
`cihai>=0.36,<0.37`.

If you need an API stabilized please [file an issue](https://github.com/cihai/cihai/issues).
:::

## Core

::::{grid} 1 1 2 2
:gutter: 2 2 3 3

:::{grid-item-card} Cihai (core)
:link: core
:link-type: doc
Application object. Bootstrap datasets, run lookups.
:::

:::{grid-item-card} Config
:link: config
:link-type: doc
Configuration loading and expansion.
:::

:::{grid-item-card} Database
:link: db
:link-type: doc
SQLAlchemy engine/session setup and helpers.
:::

:::{grid-item-card} Extend
:link: extend
:link-type: doc
Base classes for datasets and plugins.
:::

::::

## Supporting Modules

::::{grid} 1 2 3 3
:gutter: 2 2 3 3

:::{grid-item-card} Constants
:link: constants
:link-type: doc
Default paths and configuration values.
:::

:::{grid-item-card} Conversion
:link: conversion
:link-type: doc
CJK encoding conversion utilities.
:::

:::{grid-item-card} Exceptions
:link: exc
:link-type: doc
Exception hierarchy.
:::

:::{grid-item-card} Log
:link: log
:link-type: doc
Logging helpers.
:::

:::{grid-item-card} Types
:link: types
:link-type: doc
Public type aliases.
:::

:::{grid-item-card} Utils
:link: utils
:link-type: doc
Import and general utility helpers.
:::

::::

```{toctree}
:hidden:

core
config
constants
conversion
db
exc
extend
log
types
utils
```

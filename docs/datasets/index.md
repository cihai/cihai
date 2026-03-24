(datasets)=
(data)=

# Datasets

Data sources available through cihai.

::::{grid} 1 1 2 2
:gutter: 2 2 3 3

:::{grid-item-card} UNIHAN
:link: unihan
:link-type: doc
Unicode Han Database -- readings, meanings, variants.
:::

::::

## Planned datasets

For all data sets, the goal is to achieve:

- Clear and permissive a licensing for public and private use
- Compatibility with [data Packages], for data to be language agnostic and consistent
- Open source scripting used to process data into a common format

| Set       | License           | Data Package           | Project           |
| --------- | ----------------- | ---------------------- | ----------------- |
| UNIHAN    | OK [^cite_unhn-l] | OK [^cite_unhn-d]      | OK [^cite_unhn-p] |
| edict     | OK                | TODO                   | TODO              |
| cedict    | OK [^cite_cdct-l] | TODO                   | TODO              |
| cedictgr  | OK                | TODO                   | TODO              |
| handedict | OK                | TODO                   | TODO              |
| cfdict    | OK                | MISSING [^cite_cfdict] | UNKNOWN           |

[data packages]: https://specs.frictionlessdata.io/data-package/

[^cite_unhn-l]: <http://unicode.org/charts/unihan.html#Disclaimers>
[^cite_unhn-d]: <https://raw.githubusercontent.com/cihai/unihan-etl/master/datapackage.json>
[^cite_unhn-p]: <https://unihan-etl.git-pull.com/>
[^cite_cdct-l]: <https://www.mdbg.net/chinese/dictionary?page=cedict>
[^cite_cfdict]: The database at <http://www.chine-informations.com/chinois/open/CFDICT/download.php> is missing.

```{toctree}
:hidden:

unihan
```

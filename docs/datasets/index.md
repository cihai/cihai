(datasets)=
(data)=

# Datasets

```{module} cihai

```

:::{warning}
Be careful with these! Internal APIs are **not** covered by version policies. They can break or be removed between minor versions!

If you need an internal API stabilized please [file an issue](https://github.com/cihai/cihai/issues).
:::

## Current Datasets

```{toctree}
:maxdepth: 1

unihan
```

## Planned datasets

For all data sets, the goal is to achieve:

- Clear and permissive a licensing for public and private use
- Compatibility with [Data Packages][data packages], for data to be language agnostic and consistent
- Open source scripting used to process data into a common format

| Set       | License           | Data Package           | Project           |
| --------- | ----------------- | ---------------------- | ----------------- |
| UNIHAN    | OK [^cite_unhn-l] | OK [^cite_unhn-d]      | OK [^cite_unhn-p] |
| edict     | OK                | TODO                   | TODO              |
| cedict    | OK [^cite_cdct-l] | TODO                   | TODO              |
| cedictgr  | OK                | TODO                   | TODO              |
| handedict | OK                | TODO                   | TODO              |
| cfdict    | OK                | MISSING [^cite_cfdict] | UNKNOWN           |

[data packages]: http://frictionlessdata.io/data-packages/

[^cite_unhn-l]: <http://unicode.org/charts/unihan.html#Disclaimers>
[^cite_unhn-d]: <https://raw.githubusercontent.com/cihai/unihan-etl/master/datapackage.json>
[^cite_unhn-p]: <https://unihan-etl.git-pull.com/>
[^cite_cdct-l]: <https://www.mdbg.net/chinese/dictionary?page=cedict>
[^cite_cfdict]: The database at <http://www.chine-informations.com/chinois/open/CFDICT/download.php> is missing.

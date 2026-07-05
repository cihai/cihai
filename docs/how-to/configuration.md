(how-to-configuration)=

# Configure Storage

Use {meth}`cihai.core.Cihai.from_file` when configuration belongs in a JSON or YAML file instead of
inline Python. This example keeps UNIHAN disabled so the config-loading path is fast and does not
download data.

```{code-block} python

>>> import json
>>> from cihai.core import Cihai
>>> config_path = tmp_path / "cihai.json"
>>> config = {"database": {"url": "sqlite:///:memory:"}}
>>> _ = config_path.write_text(json.dumps(config))
>>> c = Cihai.from_file(config_path, unihan=False)
>>> c.config["database"]["url"]
'sqlite:///:memory:'

```

For UNIHAN bootstrap tuning, pass options directly to
{meth}`cihai.data.unihan.dataset.Unihan.bootstrap`:

```python
from cihai.core import Cihai

c = Cihai()
c.unihan.bootstrap({"fields": ["kDefinition"]})
```

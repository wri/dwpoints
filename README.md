##### DW POINTS

_CLI for generating dynamic world points values for a number of different squash techniques_

---

##### INSTALL

```bash
git clone https://github.com/wri/dwpoints.git
cd dwpoints
pip install -e .
```

---

##### USAGE


###### CLI

```bash
...
```

###### PYTHON

```python
...
```

##### CONFIG

Create custom default dwpoints config-values. Values can be updated directly through CLI, or you can edit the generated config file `dwpoints.config.yaml` directly.

...

##### DOCS

```bash
$ dwpoints --help
Usage: dwpoints [OPTIONS] COMMAND [ARGS]...

Options:
  --noisy BOOLEAN  print info and warning messages
  --help           Show this message and exit.

Commands:
  accuracy   generate accuracy results
  config     generate config file
  confusion  generate confusion matrices for specific squashes
  run        generate dwpoints file

```


```bash
$ dwpoints run --help
Usage: dwpoints run [OPTIONS] SRC [DEST]

  generate dwpoints file

Options:
  --year INTEGER         year to generate squashes
  --lon TEXT             name of longitude column
  --lat TEXT             name of latitude column
  --min_crop INTEGER     minimum number of crop months for crop-rule
  --min_cropish INTEGER  minimum number of cropish months for crop-rule
  --prefix TEXT          if no dest given, name file `{prefix}.src-
                         filename.csv`
  --noisy BOOLEAN
  --squash TEXT          comma deliminated string of squash_keys (w/o spaces)
  --help                 Show this message and exit.


```

```bash
dwpoints config --help
Usage: dwpoints config [OPTIONS]

  generate config file

Options:
  --year INTEGER         year to generate squashes
  --lon TEXT             name of longitude column
  --lat TEXT             name of latitude column
  --min_crop INTEGER     minimum number of crop months for crop-rule
  --min_cropish INTEGER  minimum number of cropish months for crop-rule
  --prefix TEXT          if not dest given, name file `{prefix}.src-
                         filename.csv`
  --noisy BOOLEAN
  --squash TEXT          comma deliminated string of squash_keys (w/o spaces)
  --force BOOLEAN        if true overwrite existing config
  --help                 Show this message and exit.
  ```





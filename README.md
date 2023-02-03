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
	DW_0	DW_1	DW_2	DW_3	DW_4	DW_5	DW_6	DW_7	DW_8	total
label										
0	0.970	0.010	0.002	0.0	0.000	0.002	0.000	0.000	0.000	500
1	0.000	0.798	0.004	0.0	0.002	0.005	0.002	0.000	0.000	500
2	0.000	0.006	0.917	0.0	0.024	0.011	0.002	0.000	0.000	500
3	0.026	0.037	0.013	1.0	0.004	0.059	0.000	0.010	0.000	500
4	0.000	0.006	0.031	0.0	0.957	0.011	0.000	0.000	0.000	500
5	0.000	0.045	0.021	0.0	0.004	0.694	0.002	0.005	0.000	500
6	0.000	0.008	0.002	0.0	0.000	0.000	0.961	0.000	0.000	500
7	0.000	0.002	0.004	0.0	0.008	0.157	0.002	0.942	0.003	500
8	0.004	0.087	0.006	0.0	0.000	0.062	0.031	0.044	0.997	500
total	507.000	618.000	519.000	412.0	494.000	657.000	514.000	412.000	367.000	4500
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





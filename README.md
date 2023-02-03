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

This repo is mainly intended to be used as a CLI, although the python modules would be useful in there own right.

###### CLI

As discussed below, specific behavior can be controled through CLI flags, or better, through a config file. In its simplest form you need an csv that has a "lon" and "lat" column:

_sample_points.csv_
```text
lon,lat
-82.02395586731994,36.11411596793721
-81.64208204004073,35.41441819313651
-86.08272398402876,35.3977095288518
```

Then you can generate the various dynamic-world labels:

```bash
$ dwpoints run sample_points.csv

[INFO] DW_POINTS: generating dynamic world point values
---------------------------------------------------------------------------------------
{'dest': 'dwpoints.sample_points.csv',
 'min_crop': 2,
 'min_cropish': 11,
 'nb_points': 3,
 'squash_columns': ['dw_mode',
                    'dw_median_label',
                    'dw_monthly_median_label_mode',
                    'dw_median_cr'],
 'src': 'sample_points.csv',
 'year': 2022}
[INFO] DW_POINTS: [[2023.02.02] 18:56:22] ...inspecting rows
[INFO] DW_POINTS: [[2023.02.02] 18:56:22] ...earthengine request (0:00:00.002666)
[INFO] DW_POINTS: [[2023.02.02] 18:56:23] complete (0:00:01.047772)
```

Which produces the csv "dwpoints.sample_points.csv":

```bash
$ cat dwpoints.sample_points.csv
dw_median_cr,dw_median_label,dw_mode,dw_monthly_median_label_mode,lat,lon
5,5,8,1,36.11411596793721,-82.02395586731994
6,6,6,6,35.41441819313651,-81.64208204004073
8,8,8,8,35.3977095288518,-86.08272398402876
```

If your sample points file contains a "label" column with the expected value you can produce an accuracy assement and confusion matrices.

_sample_points.csv_ might look like this

```text
label,lon,lat
5,-82.02395586731994,36.11411596793721
6,-81.64208204004073,35.41441819313651
8,-86.08272398402876,35.3977095288518
```

however in this example we'll use a csv saved to google cloud

```bash
$ dwpoints run https://storage.googleapis.com/dynamic-world-public/dw-exports/point_data/dev_dw_sample_pts-500.csv

[INFO] DW_POINTS: generating dynamic world point values
----------------------------------------------------------------------------------------------------
{'dest': 'dwpoints.dev_dw_sample_pts-500.csv',
 'min_crop': 2,
 'min_cropish': 11,
 'nb_points': 4500,
 'squash_columns': ['dw_mode',
                    'dw_median_label',
                    'dw_monthly_median_label_mode',
                    'dw_median_cr'],
 'src': 'https://storage.googleapis.com/dynamic-world-public/dw-exports/point_data/dev_dw_sample_pts-500.csv',
 'year': 2022}
[INFO] DW_POINTS: [[2023.02.02] 19:08:43] ...inspecting rows
[INFO] DW_POINTS: [[2023.02.02] 19:08:45] ...earthengine request (0:00:01.467955)
[INFO] DW_POINTS: [[2023.02.02] 19:10:53] complete (0:02:09.540832)
```

Now we can evaluate the accuracy and look at confusion matrices:

```bash
$dwpoints accuracy dwpoints.dev_dw_sample_pts-500.csv label      

[INFO] DW_POINTS: generating aggrement assement
----------------------------------------------------------------------------------------------------
{'dest': 'acc.dwpoints.dev_dw_sample_pts-500.csv',
 'nb_points': 4500,
 'squash_columns': ['dw_mode',
                    'dw_median_label',
                    'dw_monthly_median_label_mode',
                    'dw_median_cr'],
 'src': 'dwpoints.dev_dw_sample_pts-500.csv'}
[INFO] DW_POINTS: [[2023.02.02] 19:56:45] ...
[INFO] DW_POINTS: [[2023.02.02] 19:56:46] complete (0:00:00.084650)
```

This generated `acc.dwpoints.dev_dw_sample_pts-500.csv`.  

```python
pd.read_csv('acc.dwpoints.dev_dw_sample_pts-500.csv').set_index('label')


""" (truncated output for illustrative purposes)

        dw_median_label_acc  dw_median_cr_acc  dw_median_label_count  dw_median_cr_count  total
label                                   
0.0             0.984              0.984                492                    492         500
1.0             0.986              0.986                493                    493         500
2.0             0.952              0.952                476                    476         500
3.0             0.824              0.824                412                    412         500
4.0             0.946              0.946                473                    473         500
5.0             0.912              0.912                456                    456         500
6.0             0.988              0.988                494                    494         500
7.0             0.776              0.776                388                    388         500
8.0             0.732              0.732                366                    366         500
"""
```





```bash
    DW_0    DW_1    DW_2    DW_3    DW_4    DW_5    DW_6    DW_7    DW_8    total
label                                       
0   0.970   0.010   0.002   0.0 0.000   0.002   0.000   0.000   0.000   500
1   0.000   0.798   0.004   0.0 0.002   0.005   0.002   0.000   0.000   500
2   0.000   0.006   0.917   0.0 0.024   0.011   0.002   0.000   0.000   500
3   0.026   0.037   0.013   1.0 0.004   0.059   0.000   0.010   0.000   500
4   0.000   0.006   0.031   0.0 0.957   0.011   0.000   0.000   0.000   500
5   0.000   0.045   0.021   0.0 0.004   0.694   0.002   0.005   0.000   500
6   0.000   0.008   0.002   0.0 0.000   0.000   0.961   0.000   0.000   500
7   0.000   0.002   0.004   0.0 0.008   0.157   0.002   0.942   0.003   500
8   0.004   0.087   0.006   0.0 0.000   0.062   0.031   0.044   0.997   500
total   507.000 618.000 519.000 412.0   494.000 657.000 514.000 412.000 367.000 4500
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





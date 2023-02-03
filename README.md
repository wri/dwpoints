### DW POINTS

_CLI for generating dynamic world points values for a number of different squash techniques_

- [Install](#install)
- [CLI](#cli)
- [Example Walkthrough](#example)
- [Config](#config)
- [Docs](#docs)

---

<a href="#install"></a>
#### INSTALL

```bash
git clone https://github.com/wri/dwpoints.git
cd dwpoints
pip install -e .
```

---


<a href="#usage"></a>
#### USAGE

This repo is mainly intended to be used as a CLI, although the python modules may be used directly.

<a href="#cli"></a>
##### CLI

As discussed below, specific behavior can be controled through CLI flags, or better yet, through a config file. In its simplest form you need an csv that has a "lon" and "lat" column:

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
```

Which produces the csv "dwpoints.sample_points.csv":

```bash
$ cat dwpoints.sample_points.csv
dw_median_cr,dw_median_label,dw_mode,dw_monthly_median_label_mode,lat,lon
5,5,8,1,36.11411596793721,-82.02395586731994
6,6,6,6,35.41441819313651,-81.64208204004073
8,8,8,8,35.3977095288518,-86.08272398402876
```

If your sample points file contains a "label" column with the expected values you can produce an accuracy assement and confusion matrices by running 

```bash
$ dwpoints accuracy sample_points.csv label
$ dwpoints confusion sample_points.csv label
```

See the [walkthrough](#example) below for a detailed example of accuracy/confusion.


<a href="#example"></a>
##### EXAMPLE WALK THROUGH

This example uses some sample points in generated stored in GCS (https://storage.googleapis.com/dynamic-world-public/dw-exports/point_data/dev_dw_sample_pts-500.csv). The "label" column was generated using the annual monthly mode, which is reflected in the perfect scores shown below for `dw_mode`.

First we'll generate the dw-values:

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

This generated `dwpoints.dev_dw_sample_pts-500.csv`

![dwpoints.dev_dw_sample_pts-500.csv](https://github.com/wri/dwpoints/blob/main/images/dw_values.png?raw=true)



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

This generated `acc.dwpoints.dev_dw_sample_pts-500.csv`.  Reading it into a dataframe you'll see there is a row for each possible label value. The rows give the per-label accuracy of each squash, as well as the total correct for each squash and the total number pixels.  For clarity, note that the "\_acc" columns equal the "\_count" columns divided by the "total" column.

![accuracy output](https://github.com/wri/dwpoints/blob/main/images/acc.png?raw=true)


More useful perhaps is generating confusion matrices:


```bash
$ dwpoints confusion dwpoints.dev_dw_sample_pts-500.csv label

[INFO] DW_POINTS: generating confusion matrices
----------------------------------------------------------------------------------------------------
{'dest': 'cm.<squash>.dwpoints.dev_dw_sample_pts-500.csv',
 'nb_points': 4500,
 'squash_columns': ['dw_mode',
                    'dw_median_label',
                    'dw_monthly_median_label_mode',
                    'dw_median_cr'],
 'src': 'dwpoints.dev_dw_sample_pts-500.csv'}
[INFO] DW_POINTS: [[2023.02.02] 20:19:12] ...
- cm.dw_mode.dwpoints.dev_dw_sample_pts-500.csv
[INFO] DW_POINTS: [[2023.02.02] 20:19:12] dw_mode (0:00:00.009224)
- cm.dw_median_label.dwpoints.dev_dw_sample_pts-500.csv
[INFO] DW_POINTS: [[2023.02.02] 20:19:12] dw_median_label (0:00:00.013004)
- cm.dw_monthly_median_label_mode.dwpoints.dev_dw_sample_pts-500.csv
[INFO] DW_POINTS: [[2023.02.02] 20:19:12] dw_monthly_median_label_mode (0:00:00.016119)
- cm.dw_median_cr.dwpoints.dev_dw_sample_pts-500.csv
[INFO] DW_POINTS: [[2023.02.02] 20:19:12] dw_median_cr (0:00:00.019349)
[INFO] DW_POINTS: [[2023.02.02] 20:19:12] complete (0:00:00.019358)
```

This generated confusion matrix file for each of our different "squash" schemes listed in the `squash_columns` of the CLI output above. 

Let's have a look at the `dw_median_cr` file:

![confusion-matrix output](https://github.com/wri/dwpoints/blob/main/images/cm_sum.png?raw=true)


We can improve on this further by passing the `--normalize True` flag. You get the same result but normalized by column totals (so the diagonal values are equal to the recall):


```bash
$ dwpoints confusion dwpoints.dev_dw_sample_pts-500.csv label --normalize True

[INFO] DW_POINTS: generating confusion matrices
----------------------------------------------------------------------------------------------------
{'dest': 'cm.<squash>.dwpoints.dev_dw_sample_pts-500.csv',
 'nb_points': 4500,
 'squash_columns': ['dw_mode',
                    'dw_median_label',
                    'dw_monthly_median_label_mode',
                    'dw_median_cr'],
 'src': 'dwpoints.dev_dw_sample_pts-500.csv'}
[INFO] DW_POINTS: [[2023.02.02] 20:23:22] ...
cm-norm.dw_mode.dwpoints.dev_dw_sample_pts-500.csv
- cm-norm.dw_mode.dwpoints.dev_dw_sample_pts-500.csv
[INFO] DW_POINTS: [[2023.02.02] 20:23:22] dw_mode (0:00:00.011574)
cm-norm.dw_median_label.dwpoints.dev_dw_sample_pts-500.csv
- cm-norm.dw_median_label.dwpoints.dev_dw_sample_pts-500.csv
[INFO] DW_POINTS: [[2023.02.02] 20:23:22] dw_median_label (0:00:00.017708)
cm-norm.dw_monthly_median_label_mode.dwpoints.dev_dw_sample_pts-500.csv
- cm-norm.dw_monthly_median_label_mode.dwpoints.dev_dw_sample_pts-500.csv
[INFO] DW_POINTS: [[2023.02.02] 20:23:22] dw_monthly_median_label_mode (0:00:00.022811)
cm-norm.dw_median_cr.dwpoints.dev_dw_sample_pts-500.csv
- cm-norm.dw_median_cr.dwpoints.dev_dw_sample_pts-500.csv
[INFO] DW_POINTS: [[2023.02.02] 20:23:22] dw_median_cr (0:00:00.027556)
[INFO] DW_POINTS: [[2023.02.02] 20:23:22] complete (0:00:00.027568)
```

![confusion-matrix output](https://github.com/wri/dwpoints/blob/main/images/cm_norm.png?raw=true)


<a href="#python"></a>
##### PYTHON

If need be you can access the same functionality through the python modules.
```python
import dwpoints.core as core
import dwpoints.labels as labels

...
```

<a href="#python"></a>
#### CONFIG

Create custom default dwpoints config-values. Values can be updated directly through CLI, or you can edit the generated config file `dwpoints.config.yaml` directly. I suggest generating the file with the default values and editing the resulting YAML file:

```bash
$ dwpoints config             
[INFO] DW_POINTS: dwpoints-config.yaml created. edit file to change configuration
$ cat dwpoints-config.yaml
# dwpoints: config
lat: lat
lon: lon
min_crop: 2
min_cropish: 11
noisy: true
prefix: dwpoints
squash_keys:
- dw_mode
- dw_median_label
- dw_monthly_median_label_mode
- dw_median_cr
year: 2022
```

Now you can edit this file to change the "squash_keys" or the "year", or change the "lon/lat" naming convention to "longitude/latitude" etc.

Note all these choices can be overridden using args and flags for the CLI (See [docs](#docs) below for more detail). That said having fixed config files will be the easiest approach.


<a href="#docs"></a>
#### DOCS

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
$ dwpoints config --help
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

```bash
$ dwpoints accuracy --help
Usage: dwpoints accuracy [OPTIONS] SRC LABEL

  generate accuracy results

Options:
  --prefix TEXT    output file is `{prefix}.src-filename.csv`
  --noisy BOOLEAN
  --squash TEXT    comma deliminated string of squash_keys (w/o spaces)
  --help           Show this message and exit.
```

```bash
$ dwpoints confusion --help
Usage: dwpoints confusion [OPTIONS] SRC LABEL

  generate confusion matrices for specific squashes

Options:
  --prefix TEXT        output files are `{prefix}.{squash_col}.src-
                       filename.csv`
  --noisy BOOLEAN
  --squash TEXT        comma deliminated string of squash_keys (w/o spaces)
  --normalize BOOLEAN  normalize confusion matrix
  --help               Show this message and exit.
  ```





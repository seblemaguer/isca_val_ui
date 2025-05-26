# ISCA Publication checker UI

This repository contains a Qt UI to facilitate the validation and the correction of the metadata for any ISCA conference (for now, only Interspeech is supported).

## How to install
It should be installed through pip for now

```sh
pip install isca-val-ui
```

## How to run

Go to the directory of the validation package, and run the following command

```sh
isca_val_ui
```

By default, the report is assumed to be in `report.yaml`.
It is possible to defined a different report file:

```sh
isca_val_ui -r <the report file.yaml>
```

## Some bugs?

The tool has only be tested on ubuntu/wayland and more test would be welcomed

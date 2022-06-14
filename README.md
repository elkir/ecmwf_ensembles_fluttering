_Author: Petr Dolezal Date:2022-06-12_

As a part of the ECMWF 2022 Visualization hackathon, I tried to develop new ways to display the data held in multiple ensemble members.

I've developped a way to animate the datasets to show the predictions of different ensemble members as a flutter at each time step visualization.

The script developped to generate the videos presented can be found in the `export_flutter_*.py` files which use functions in the `flutter.py` module.

Scripts must be run in an environment specified in `environment.yml`:
```
conda env create --file environment.yml
conda activate hack_2022_ecmwf_fluttering
```
Data downloaded from https://get.ecmwf.int/#browse/browse:vishackathon (Thanks to Milana Vuckovic for providing them)

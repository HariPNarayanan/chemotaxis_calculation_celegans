# Chemotaxis Index Analysis

This script processes CSV files containing the output of an ImageJ pipeline that utilizes TrackMate to quantify the trajectories of a group of behaving _C elegans_ and computes a chemotaxis index per track.

## What It Does

- Reads `T_*.csv` and `S_*.csv` files (the track and spot files of the TrackMate output respectively, renamed to ensure that the prefix convention is maintained).
- Extracts relevant metrics like distance traveled and final Y position.
- Merges data and computes the **Chemotaxis Index**:
  
    Chemotaxis Index = (1100 − Y_final) / Distance Traveled
    where 1100 is a fixed value of y in the output files established to be the centre of the plate locked to the setup. This will likely vary across setups with different camera and arena combinations.

- Outputs results to `analysed.csv` in the same directory.

## Folder Structure

```text
chemotaxis_calculation_celegans/
├── chemotaxis_calculation_celegans.py
├── chemotaxis_calculation_celegans.ipynb
├── example_data/
│   ├── T_example.csv
│   └── S_example.csv
└── README.md
```

## Example Usage

1. Run the script:
    ```
    python chemotaxis_calculation_celegans.py
    ```

2. Select the `example_data/` folder when prompted.

3. Output:
   - A file `analysed.csv` will be generated in the same folder containing:
     ```csv
     TRACK_ID	Distance	Label	Source	Y	Chemotaxis
     0	2625.09301	Worm 1	Example.csv	747.5339113	0.134268038
     1	2258.569086	Worm 2	Example.csv	894.7455645	0.090878086
     2	2550.231664	Worm 3	Example.csv	755.3596711	0.135140793
     3	1136.138362	Worm 4	Example.csv	860.415811	0.210875891
     4	2391.65831	Worm 5	Example.csv	612.6770666	0.20375943
     5	2471.94398	Worm 6	Example.csv	877.3658353	0.090064405
     6	2117.286487	Worm 7	Example.csv	926.6180694	0.081888744
     8	2260.789821	Worm 8	Example.csv	857.9233859	0.107076125
     10	2223.61585	Worm 9	Example.csv	954.8182036	0.065290862
     11	2383.967349	Worm 10	Example.csv	863.0634415	0.099387502
     ```

## Requirements

- Python 3.x
- pandas
- tkinter

Install dependencies if needed:
```
pip install pandas
pip install tkinter
```
## Citations for TrackMate 

Ershov, D., Phan, M.-S., Pylvänäinen, J. W., Rigaud, S. U., Le Blanc, L., Charles-Orszag, A., … Tinevez, J.-Y. (2022). TrackMate 7: integrating state-of-the-art segmentation algorithms into tracking pipelines. Nature Methods, 19(7), 829–832. doi:10.1038/s41592-022-01507-1

and 

Tinevez, J.-Y., Perry, N., Schindelin, J., Hoopes, G. M., Reynolds, G. D., Laplantine, E., … Eliceiri, K. W. (2017). TrackMate: An open and extensible platform for single-particle tracking. Methods, 115, 80–90. doi:10.1016/j.ymeth.2016.09.016

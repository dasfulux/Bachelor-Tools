# Bachelor-Tools

A small collection of Python scripts used to process `.yaml` files for my Bachelor's thesis.

All scripts are located in the [`src`](src) directory.

⚠️ These scripts assume that the YAML files follow the expected structure. Incorrectly formatted files may cause errors.


## count_hcp.py

Counts the number of HCP entries in a YAML file.

### Usage
```bash
python3 src/coun_hcp.py <path/to/file.yaml>
```


## remove_tagged.py

Removes all HCP entries that contain tags, or only entries with specific tags.

The script does not modify the original file. Instead, it writes the filtered output to a new file in the `output` directory.

If the directory does not exist, it will be created automatically.

### Usage
```bash
python3 remove_tagged.py <path/to/file.yaml> [<tag1> <tag2> ...]
```


## hcp_to_location.py

Extracts the locations from a HCP list and creates a new file holding these locations. The locations that are put out are in format `file:lineno:colno_start-lineno:colno_end`. 

The file is put in the `output` directory. If the directory does not exist, it will be created automatically.

### Usage
```bash
python3 hcp_to_location.py <path/to/file.yaml>
```

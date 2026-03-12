import os
import sys
import yaml

"""
Takes a yaml list, and creates a new list with only the locations.
"""
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 <python_script> <filepath>")
        sys.exit(1)
    
    filepath = sys.argv[1]

    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    locations = []
    for value in data.values():
        for hcp in value:
            location = hcp.get('Location')
            varname = hcp.get('VarName', "")
            vartype = hcp.get('Type', "")

            if location:
                filename = location.get('Filename', None)
                lineno = location.get('Lineno', None)

                colno_start = location.get('Colno', None)
                colno_end = colno_start + len(varname)  + len(vartype)

                path = f"{filename}:{lineno}:{colno_start}-{lineno}:{colno_end}"
                locations.append({
                    "VarName": varname,
                    "Location": path
                })
            else:
                print(f"Error: Not a valid location - {hcp}")

    base = os.path.basename(filepath)
    name, ext = os.path.splitext(base)
    new_name = f"{name}_locations{ext}"
    out_path = os.path.join('src/output', new_name)

    os.makedirs('src/output', exist_ok=True)

    with open(out_path, 'w') as f:
        yaml.safe_dump(locations, f, sort_keys=False)


if __name__ == "__main__":
    main()

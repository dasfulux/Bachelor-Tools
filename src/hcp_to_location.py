import argparse
import os
import yaml

literal_cnt = 0

def main():
    args = parse_args()

    try:
        filepath = args.filepath
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)

    locations = []
    for value in data.values():
        for hcp in value:
            location = hcp.get('Location')
            varname = hcp.get('VarName', gen_literal_name())
            vartype = hcp.get('Type', "")

            if location:
                filename = location.get('Filename', None)
                lineno = location.get('Lineno', None)

                if "LiteralBinOp" in varname:
                    colno_start = 1
                else:
                    colno_start = location.get('Colno', None)
                colno_end = colno_start + len(varname)  + len(vartype)

                path = f"{filename}:{lineno}:{colno_start}-{lineno}:{colno_end+2}"
                locations.append({
                    "VarName": varname,
                    "Location": path,
                })
            else:
                print(f"Error: Not a valid location - {hcp}")

    out_path = args.output
    out_dir = os.path.dirname(out_path)

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(out_path, 'w') as f:
        yaml.safe_dump(locations, f, sort_keys=False)


def gen_literal_name():
    global literal_cnt
    literal_name = f"LiteralBinOp{literal_cnt}"
    literal_cnt += 1
    return literal_name


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a YAML list containing only location entries."
    )
    
    parser.add_argument("filepath", help="Path to the input YAML file")
    parser.add_argument("-n", "--name", help="Name to give the file")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Path to output file. If omitted, a name is auto-generated in src/output/.",
    )

    args = parser.parse_args()

    # Default to src/output/
    if args.output is None:
        base = os.path.basename(args.filepath)
        name, ext = os.path.splitext(base)
        new_name = f"{name}_locations{ext}"
        args.output = os.path.join("src/output", new_name)

    return args


if __name__ == "__main__":
    main()

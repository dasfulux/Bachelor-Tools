import argparse
import os
import subprocess
import yaml

"""
python3 Bachelor_Tools/src/temp.py src/FMstimator.py eval/FastDownward_eval/repo/ eval/FastDownward_eval/locations/FCP-HC-FastDownward-FDDriverPy-113fe1a626_4e3852e3-40e2-493e-866a-30377a09cee0_success_filtered_all_locations.yaml 113fe1a626176f0c34888c645d4c25e7c31db372
"""

def main():
    args = parse_args()

    # Load YAML
    with open(args.locations, "r") as f:
        data = yaml.safe_load(f)

    # Ensure output directory exists
    os.makedirs(args.output, exist_ok=True)

    # Loop over all entries
    for entry in data:
        varname = entry.get("VarName")
        location = entry.get("Location")

        if not varname or not location:
            print(f"Skipping invalid entry: {entry}")
            continue

        # Working thing, to be removed
        # if "Literal" in varname:
        #    print(f"skipping literals for now")
        #    continue

        # Build command
        cmd = [
            args.FMstimator,
            args.repo,
            location,
            args.commit,
            "-n", varname,
            "-o", args.output
        ]

        print("Running:", " ".join(cmd))

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running FMstimator for {varname}: {e}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Remove entries with specific tags from YAML lists."
    )
    
    parser.add_argument("FMstimator", help="Path to the FMstimator")
    parser.add_argument("repo", help="Path to the repo")
    parser.add_argument("locations", help="Path to the YAML with the input locations")
    parser.add_argument("commit", help="")

    parser.add_argument(
        "-o",
        "--output",
        default="src/output",
        help="Path to output file. If omitted, a name is auto-generated in src/output/.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()

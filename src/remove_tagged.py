import argparse
import os
import yaml


def main():
    """
    Remove entries with specific tags from YAML lists and save the cleaned data to new files.
    """
    args = parse_args()

    try:
        filepath = args.filepath
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)

    tags_to_remove = args.tags
    filtered_data = {}
    for key, value in data.items():
        if isinstance(value, list):
            filtered_list = []
            for entry in value:
                if not isinstance(entry, dict):
                    filtered_list.append(entry)
                    continue

                entry_tags = entry.get("tags", []) or []
                if tags_to_remove:
                    if any(tag in tags_to_remove for tag in entry_tags):
                        continue
                else:
                    if entry_tags:
                        continue
                filtered_list.append(entry)

            filtered_data[key] = filtered_list
        else:
            filtered_data[key] = value

    out_path = args.output
    out_dir = os.path.dirname(out_path)
    if out_dir:
        # Create output directory if not yet present
        os.makedirs(out_dir, exist_ok=True)

    with open(out_path, 'w') as f:
        yaml.safe_dump(filtered_data, f, sort_keys=False)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Remove entries with specific tags from YAML lists."
    )
    
    parser.add_argument("filepath", help="Path to the input YAML file")
    parser.add_argument(
        "tags",
        nargs="*",
        help="Tags to remove. If omitted, all tagged entries are removed.",
    )
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
        if args.tags:
            tag_part = "_".join(args.tags)
            new_name = f"{name}_filtered_{tag_part}{ext}"
        else:
            new_name = f"{name}_filtered_all{ext}"
        args.output = os.path.join("src/output", new_name)

    return args


if __name__ == "__main__":
    main()
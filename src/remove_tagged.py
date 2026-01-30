import os
import sys
import yaml

"""
Remove entries with specific tags from YAML lists and save the cleaned data to new files.
"""
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 <python_script> <filepath> [<tag1> <tag2> ...]")
        sys.exit(1)
    
    filepath = sys.argv[1]

    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    if len(sys.argv) < 3:
        tags_to_remove = []  # No tags specified, remove all tagged entries
    else:
        tags_to_remove = sys.argv[2:]  # Tags specified as command-line arguments; overkill but fancy

    filtered_data = {}
    for key, value in data.items():
        if isinstance(value, list):
            filtered_list = []
            for entry in value:
                if not isinstance(entry, dict):
                    filtered_list.append(entry)
                    continue

                entry_tags = entry.get('tags', []) or []
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

    base = os.path.basename(filepath)
    name, ext = os.path.splitext(base)
    if tags_to_remove:
        new_name = f"{name}_filtered_{tags_to_remove}{ext}"
    else:
        new_name = f"{name}_filtered_all{ext}"
    out_path = os.path.join('src/output', new_name)

    os.makedirs('src/output', exist_ok=True)

    with open(out_path, 'w') as f:
        yaml.safe_dump(filtered_data, f, sort_keys=False)


if __name__ == "__main__":
    main()
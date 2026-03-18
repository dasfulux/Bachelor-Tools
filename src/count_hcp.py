import argparse
import yaml


def main():
    """
    Count total and untagged entries in YAML lists.
    Does not count by tags.
    """
    args = parse_args()
 
    try:
        filepath = args.filepath
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)
    
    lists_to_count = {key: value for key, value in data.items() if isinstance(value, list)}
    overall_total = sum(len(entries) for entries in lists_to_count.values())
    overall_untagged = sum(1 for entries in lists_to_count.values() for entry in entries if not entry.get('tags'))

    print(f"Total entries: {overall_total}\n")
    print(f"Untagged entries: {overall_untagged}\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Count total and untagged entries in YAML lists."
    )
    
    parser.add_argument("filepath", help="Path to the input YAML file")
    
    return parser.parse_args()


if __name__ == "__main__":
    main()

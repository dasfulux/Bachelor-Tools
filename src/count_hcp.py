import sys
import yaml

""""
Count total and untagged entries in YAML lists.
Does not count by tags.
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
    
    lists_to_count = {key: value for key, value in data.items() if isinstance(value, list)}
    overall_total = sum(len(entries) for entries in lists_to_count.values())
    overall_untagged = sum(1 for entries in lists_to_count.values() for entry in entries if not entry.get('tags'))

    print(f"Total entries: {overall_total}")
    print(f"Untagged entries: {overall_untagged}")


if __name__ == "__main__":
    main()

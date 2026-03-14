import json
from pathlib import Path

def reconstruct_splits(regvd_dir: Path, output_file_json: Path):
    splits_reveal = {}
    
    # Files to process
    files = {
        "train": regvd_dir / "train.jsonl",
        "valid": regvd_dir / "valid.jsonl",
        "test": regvd_dir / "test.jsonl"
    }
    
    for split_name, file_path in files.items():
        if not file_path.exists():
            print(f"Warning: {file_path} not found.")
            continue
            
        print(f"Processing {file_path}...")
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    idx = data.get("idx")
                    if idx is not None:
                        # Key must be string for JSON compatibility
                        splits_reveal[str(idx)] = split_name
                    else:
                        print(f"Warning: 'idx' missing in entry: {line[:50]}...")
                except json.JSONDecodeError:
                    print(f"Error decoding line: {line[:50]}...")

    # Sort keys for readability
    sorted_splits = dict(sorted(splits_reveal.items(), key=lambda item: int(item[0])))
    
    # Save to JSON
    output_file_json.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file_json, "w", encoding="utf-8") as f:
        json.dump(sorted_splits, f, indent=4)
    print(f"Successfully reconstructed splits and saved to {output_file_json}")

    # Save to CSV
    output_file_csv = output_file_json.parent / "splits.csv"
    with open(output_file_csv, "w", encoding="utf-8") as f:
        f.write("index,split\n")
        for idx, split in sorted_splits.items():
            f.write(f"{idx},{split}\n")
    print(f"Successfully reconstructed splits and saved to {output_file_csv}")
    
    print(f"Total entries: {len(splits_reveal)}")

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    regvd_path = project_root / "data" / "devign"
    output_path_json = project_root / "data" / "v0" / "splits_reveal.json"
    
    reconstruct_splits(regvd_path, output_path_json)

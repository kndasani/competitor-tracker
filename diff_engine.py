import os
import difflib
from typing import Tuple, Optional

def get_latest_snapshots(domain_prefix: str, snapshot_dir: str = "snapshots") -> Tuple[Optional[str], Optional[str]]:
    """
    Finds the two most recent snapshot files for a given domain prefix.
    Returns (latest_filepath, previous_filepath).
    """
    if not os.path.exists(snapshot_dir):
        return None, None

    files = [
        os.path.join(snapshot_dir, f)
        for f in os.listdir(snapshot_dir)
        if f.startswith(domain_prefix) and f.endswith(".md")
    ]

    # Sort files chronologically by filename (timestamp embedded in name)
    files.sort()

    if len(files) < 2:
        latest = files[-1] if len(files) == 1 else None
        return latest, None

    return files[-1], files[-2]

def compute_text_diff(old_filepath: str, new_filepath: str) -> str:
    """
    Compares two Markdown snapshot files and returns only added/modified lines.
    """
    with open(old_filepath, "r", encoding="utf-8") as f:
        old_lines = f.readlines()

    with open(new_filepath, "r", encoding="utf-8") as f:
        new_lines = f.readlines()

    diff = list(difflib.unified_diff(
        old_lines, 
        new_lines, 
        fromfile=os.path.basename(old_filepath), 
        tofile=os.path.basename(new_filepath), 
        lineterm=""
    ))

    # Filter for added lines only (lines starting with '+' but not '+++')
    added_lines = [
        line[1:].strip() 
        for line in diff 
        if line.startswith("+") and not line.startswith("+++") and line[1:].strip()
    ]

    return "\n".join(added_lines)

if __name__ == "__main__":
    domain_prefix = "github_com"
    latest, previous = get_latest_snapshots(domain_prefix)

    print(f"Latest Snapshot: {latest}")
    print(f"Previous Snapshot: {previous}")

    if latest and previous:
        diff_result = compute_text_diff(previous, latest)
        print("\n--- Detected Delta (Additions) ---")
        print(diff_result[:500] if diff_result else "No changes detected between snapshots.")
    else:
        print("\nNeed at least two snapshots to compute a diff.")
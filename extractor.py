import os
from datetime import datetime
from dotenv import load_dotenv
from parallel import Parallel

load_dotenv()

def extract_and_save(url: str, snapshot_dir: str = "snapshots") -> str:
    """
    Extracts Markdown content from a URL via Parallel Extract API 
    and saves it to a timestamped file in the snapshot directory.
    """
    api_key = os.getenv("PARALLEL_API_KEY")
    if not api_key:
        raise ValueError("PARALLEL_API_KEY not found in environment variables.")

    client = Parallel(api_key=api_key)
    print(f"Fetching content from: {url}...")

    result = client.extract(urls=[url])
    markdown_content = ""

    if hasattr(result, "results") and result.results:
        first_result = result.results[0]

        # Parallel Extract returns content in excerpts list
        if hasattr(first_result, "excerpts") and first_result.excerpts:
            markdown_content = "\n\n".join(first_result.excerpts)
        elif isinstance(first_result, dict):
            excerpts = first_result.get("excerpts", [])
            markdown_content = "\n\n".join(excerpts) if excerpts else first_result.get("full_content", "")

    if not markdown_content:
        raise RuntimeError("Extraction failed or returned empty content.")

    # Ensure snapshot directory exists
    os.makedirs(snapshot_dir, exist_ok=True)

    # Generate a clean filename based on domain and timestamp
    domain_clean = url.split("//")[-1].split("/")[0].replace(".", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{domain_clean}_{timestamp}.md"
    filepath = os.path.join(snapshot_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"Snapshot saved successfully: {filepath}")
    return filepath

if __name__ == "__main__":
    test_url = "https://github.com/readme"
    try:
        saved_path = extract_and_save(test_url)
        print(f"\nSUCCESS! Extraction passed. Saved file: {saved_path}")
    except Exception as e:
        print(f"Error during extraction and save: {e}")
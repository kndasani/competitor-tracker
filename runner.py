import sys
from extractor import extract_and_save
from diff_engine import get_latest_snapshots, compute_text_diff
from analyzer import analyze_diff_content
from notifier import send_slack_notification

def process_competitor_url(url: str):
    """
    Runs the complete competitive intelligence pipeline for a target URL.
    """
    print(f"\n==========================================")
    print(f" Processing Target: {url}")
    print(f"==========================================")

    # 1. Extract and save new snapshot
    snapshot_path = extract_and_save(url)

    # 2. Derive domain prefix to locate snapshots
    domain_prefix = url.split("//")[-1].split("/")[0].replace(".", "_")
    latest, previous = get_latest_snapshots(domain_prefix)

    if not previous:
        print("\n[INFO] Baseline snapshot created. Run the runner again on this URL after page changes occur to generate delta analysis.")
        return

    # 3. Compute text additions/deltas
    print(f"\nComparing latest ({latest}) with previous ({previous})...")
    diff_text = compute_text_diff(previous, latest)

    if not diff_text or diff_text.strip() == "":
        print("\n[RESULT] No new changes detected between consecutive snapshots.")
        return

    # 4. Run LLM PM Analysis on detected changes
    print("\nAnalyzing changes with Gemini Flash...")
    analysis = analyze_diff_content(diff_text, url)

    print("\n==========================================")
    print("        COMPETITOR UPDATE DETECTED        ")
    print("==========================================")
    print(f"URL: {url}")
    print(f"Category:     {analysis.category}")
    print(f"Impact Level: {analysis.impact_level}")
    print(f"Summary:      {analysis.summary}")
    print("\nKey Takeaways:")
    for takeaway in analysis.key_takeaways:
        print(f"  • {takeaway}")
    print("==========================================\n")

    # 5. Deliver notification to Slack
    print("Delivering competitive update notification...")
    send_slack_notification(analysis, url)

if __name__ == "__main__":
    test_url = "https://github.com/readme"
    process_competitor_url(test_url)